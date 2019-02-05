import numpy as np
import xlwings as xw
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import pandas as pd
import math
from flask import Flask, request, jsonify
app = Flask(__name__)


def planilha1(jsonValues):
	num_produtos = 10
	num_linhas = 3
	nome_colunas = ['E','F','G','H','I','J','K','L','M','N']

	#custo de produção na linha l
	try:
		c = [[ int(0) for _ in range(num_linhas)]for _ in range(num_produtos)]
		index_i = 0
		for i in nome_colunas:
			ii = 27
			index_j = 0
			for j in range(3):
				c[index_i][index_j] = float(jsonValues['{}{}'.format(i,ii)].replace(",","."))
				ii += 1
				index_j += 1
			index_i += 1

		#preco venda
		l = [ float(0) for _ in range(num_produtos)]
		ii = 0
		for i in nome_colunas:
			l[ii] = float(jsonValues['{}9'.format(i)].replace(",","."))
			ii += 1

		#demanda
		d = [ float(0) for _ in range(num_produtos)]
		ii = 0
		for i in nome_colunas:
			d[ii] = float(jsonValues['{}19'.format(i)].replace(",","."))
			ii += 1

		#demanda_superior
		d_s = [ float(0) for _ in range(num_produtos)]
		ii = 0
		for i in nome_colunas:
			valor = float(jsonValues['{}20'.format(i)].replace(",","."))
			d_s[ii] = int(d[ii]*(1+valor))
			ii += 1

		#demanda_inferior
		d_i = [ float(0) for _ in range(num_produtos)]
		ii = 0
		for i in nome_colunas:
			valor = float(jsonValues['{}21'.format(i)].replace(",","."))
			d_i[ii] =  math.ceil(d[ii]*(1-valor))
			ii += 1

		#capacidade de produção nas linhas para cada produto
		p = [[ int(0) for _ in range(num_linhas)]for _ in range(num_produtos)]
		index_i = 0
		for i in nome_colunas:
			ii = 23
			index_j = 0
			for j in range(3):
				p[index_i][index_j] = float(jsonValues['{}{}'.format(i,ii)].replace(",","."))
				ii += 1
				index_j += 1
			index_i += 1

		profit = []
		nomes = []
		types =[]
		po = "MAX "

		for i in range(num_produtos):
			for j in range(num_linhas):
				exec("nomes.append('x_%s_%s')" % (i,j))
				profit.append((l[i]-c[i][j])/l[i])
				types.append('N')



		expr = []
		coeficientes = []
		senses = []
		lista_aux = []
		lista_geral = []
		rhs = []
		names= []
		pp = 0

		#demanda
		for i in range(num_produtos):
			expr = []
			coeficientes = []
			for j in range(num_linhas):
				exec("expr.append('x_%s_%s')" % (i,j))
				coeficientes.append(1)
			senses.append('G')
			exec("names.append('c_%s')" % (pp))
			rhs.append(d_i[i])
			lista_aux = [expr,coeficientes]
			lista_geral += [lista_aux]
			pp+=1
			senses.append('L')
			exec("names.append('c_%s')" % (pp))
			rhs.append(d_s[i])
			lista_aux = [expr,coeficientes]
			lista_geral += [lista_aux]
			pp+=1

		#capacidade produtiva

		for i in range(num_produtos):
			for j in range(num_linhas):
				expr = []
				coeficientes = []
				exec("expr.append('x_%s_%s')" % (i,j))
				coeficientes.append(1)
				if(c[i][j] == 0 or p[i][j] == 0):
					senses.append('E')
					exec("names.append('c_%s')" % (pp))
					rhs.append(0)
					lista_aux = [expr,coeficientes]
					lista_geral += [lista_aux]
					pp+=1
				else:
					senses.append('L')
					exec("names.append('c_%s')" % (pp))
					rhs.append(p[i][j])
					lista_aux = [expr,coeficientes]
					lista_geral += [lista_aux]
					pp+=1

		resp_obj = {}
		resp_obj['Optma'] = {}
		try:
			# print(names)
			prob = cplex.Cplex()
			prob.objective.set_sense(prob.objective.sense.maximize)
			prob.variables.add(obj = profit,
						  types = types,
						  names = nomes)

			prob.linear_constraints.add(lin_expr = lista_geral,
								senses = senses,
								rhs = rhs,
								names = names)

			# prob.set_log_stream(None)
			# prob.set_error_stream(None)
			# prob.set_warning_stream(None)
			# prob.set_results_stream(None)
			cellset = {}
			# prob.parameters.timelimit.set(60)
			# prob.write("lpex1.lp")
			prob.solve()
			row = prob.solution.get_values()
			index = 0
			for i in range(num_produtos):
				ii = 31
				for j in range(num_linhas):
					resp_obj['Optma']['{}{}'.format(nome_colunas[i],ii)] = row[index]
					ii += 1
					index += 1
			# print(row)
		except CplexError as exc:
			resp_obj['Optma']['O17'] = "error"

		return resp_obj
	except:
		resp_obj = {}
		resp_obj['Optma'] = {}
		resp_obj['Optma']['O17'] = "erro nos dados"
		return resp_obj

@app.route("/planilha1", methods=['POST','GET'])
def mainPlanilha1():
	resp_obj = planilha1(request.json)
	return jsonify(resp_obj)

if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True, port=5980)