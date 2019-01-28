import numpy as np
import xlwings as xw
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import pandas as pd

def miniOptima():
	# wb = xw.Book(r'C:/Users/Usuario/Documents/Mini Optma/planilha3.xlsx')
	wb = xw.Book.caller()

	Sheet1 = wb.sheets[0]

	meta_lucro = float(Sheet1.range('H15').value)
	meta_custo = float(Sheet1.range('J16').value)

		
	c = []
	custos = Sheet1.range('B:B')[1:13].value
	for custo in custos:
		c.append(float(custo)) 


	l = []
	lucros = Sheet1.range('C:C')[1:13].value
	for lucro in lucros:
		l.append(float(lucro)) 

	d = []
	vendas = Sheet1.range('D:D')[1:13].value
	for venda in vendas:
		d.append(float(venda)) 
	# In[7]:

	p = []
	elaticidades = Sheet1.range('G:G')[1:13].value
	for elaticidade in elaticidades:
		p.append(float(elaticidade)) 


	num_produtos = len(l)


	
	profit = []
	nomes = []
	types =[]
	profit2 = []
	nomes2 = []
	types2 =[]
	po = "MAX "

	for i in range(num_produtos):
		exec("nomes.append('x_%s')" % (i))
		profit.append(c[i])
		types.append('N')
		exec("nomes2.append('x_%s')" % (i))
		profit2.append(c[i]*l[i])
		types2.append('N')


	expr = []
	coeficientes = []
	senses = []
	lista_aux = []
	lista_geral = []
	rhs = []
	names= []

	expr2 = []
	coeficientes2 = []
	senses2 = []
	lista_aux2 = []
	lista_geral2 = []
	rhs2 = []
	names2= []
	pp = 0

	#demanda
	for i in range(num_produtos):
		exec("expr.append('x_%s')" % (i))
		coeficientes.append(c[i] * l[i])
		exec("expr2.append('x_%s')" % (i))
		coeficientes2.append(c[i])
	senses.append('G')
	exec("names.append('c_%s')" % (pp))
	rhs.append(meta_lucro)
	lista_aux = [expr,coeficientes]
	lista_geral += [lista_aux]
	senses2.append('L')
	exec("names2.append('c_%s')" % (pp))
	rhs2.append(meta_custo)
	lista_aux2 = [expr2,coeficientes2]
	lista_geral2 += [lista_aux2]
	pp+=1


	# In[11]:


	for i in range(num_produtos):
		# P/ META LUCRO
		# Demanda maxima
		
		expr = []
		coeficientes = []
		exec("expr.append('x_%s')" % (i))
		coeficientes.append(1)
		senses.append('L')
		rhs.append(d[i]*(1+p[i]))
		exec("names.append('c_%s')" % (pp))
		lista_aux = [expr,coeficientes]
		lista_geral += [lista_aux]
		pp += 1

		# Demanda minima
		expr = []
		coeficientes = []
		exec("expr.append('x_%s')" % (i))
		coeficientes.append(1)
		senses.append('G')
		rhs.append(d[i]*(1-p[i]))
		exec("names.append('c_%s')" % (pp))
		lista_aux = [expr,coeficientes]
		lista_geral += [lista_aux]
		pp += 1
		
		
		# P/ META CUSTO
		# Demanda maxima
		expr2 = []
		coeficientes2 = []
		exec("expr2.append('x_%s')" % (i))
		coeficientes2.append(1)
		senses2.append('L')
		rhs2.append(d[i]*(1+p[i]))
		exec("names2.append('c_%s')" % (pp))
		lista_aux2 = [expr2,coeficientes2]
		lista_geral2 += [lista_aux2]
		pp += 1

		# Demanda minima
		expr2 = []
		coeficientes2 = []
		exec("expr2.append('x_%s')" % (i))
		coeficientes2.append(1)
		senses2.append('G')
		rhs2.append(d[i]*(1-p[i]))
		exec("names2.append('c_%s')" % (pp))
		lista_aux2 = [expr2,coeficientes2]
		lista_geral2 += [lista_aux2]
		pp += 1
	


	try:
		# print(names)
		prob = cplex.Cplex()
		prob.objective.set_sense(prob.objective.sense.minimize)
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
		prob.solve()
		row = prob.solution.get_values()

		total_lucros = 0
		ii = 2
		jj = 0
		for i in row:
			Sheet1.range('H{}'.format(ii)).value = i
			total_lucros += i *c[jj]*l[jj]
			ii += 1
			jj += 1

		Sheet1.range('H15').value = total_lucros
		# print(row)
	except CplexError as exc:
		Sheet1.range('L1').value = 'Não foi encontrada solução viável'


	try:
		# print(names)
		prob2 = cplex.Cplex()
		prob2.objective.set_sense(prob2.objective.sense.maximize)
		prob2.variables.add(obj = profit2,
					  types = types2,
					  names = nomes2)

		prob2.linear_constraints.add(lin_expr = lista_geral2,
							senses = senses2,
							rhs = rhs2,
							names = names2)

		# prob.set_log_stream(None)
		# prob.set_error_stream(None)
		# prob.set_warning_stream(None)
		# prob.set_results_stream(None)
		cellset = {}
		# prob.parameters.timelimit.set(60)
		prob2.solve()
		row = prob2.solution.get_values()
		total_custos = 0
		ii = 2
		jj = 0
		for i in row:
			Sheet1.range('J{}'.format(ii)).value = i
			total_custos += i *c[jj]
			ii += 1
			jj += 1
		Sheet1.range('J16').value = total_custos
		Sheet1.range('N2').value = ''
		# print(row)
	except CplexError as exc:
		Sheet1.range('N2').value = 'Não foi encontrada solução viável'


# if __name__ == "__main__":
#   rand_numbers()
