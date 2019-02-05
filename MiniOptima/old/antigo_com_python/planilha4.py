import numpy as np
import xlwings as xw
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import pandas as pd

def miniOptima():
	# wb = xw.Book(r'C:/Users/Usuario/Documents/Mini Optma/planilha4.xlsx')
	wb = xw.Book.caller()

	Sheet1 = wb.sheets[0]
	Sheet2 = wb.sheets[1]
	Sheet3 = wb.sheets[2]

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

	h = [[ int(0) for _ in range(2)]for _ in range(num_produtos)]
	Produtos = Sheet3.range('A:A')[1:13].value
	Linhas = Sheet3.range('B:B')[1:13].value
	Tempos = Sheet3.range('C:C')[1:13].value
	i = 0
	for tempo in Tempos:
		h[int(Produtos[i]-1)][int(Linhas[i]-1)] = float(tempo)
		i+=1

	array_multas = Sheet2.range('F:F')[1:3].value
	multa = []
	for array_multa in array_multas:
		multa.append(float(array_multa)) 


	array_capacidades = Sheet2.range('B:B')[1:3].value
	capacidade = []
	for array_capacidade in array_capacidades:
		capacidade.append(float(array_capacidade)) 



	array_extras = Sheet2.range('G:G')[1:3].value
	extras = []
	for extra in array_extras:
		extras.append(float(extra)) 



	profit = []
	nomes = []
	types =[]
	profit2 = []
	nomes2 = []
	types2 =[]
	profit3 = []
	nomes3 = []
	types3 =[]
	po = "MAX "

	for i in range(num_produtos):
		exec("nomes.append('x_%s')" % (i))
		profit.append(c[i])
		types.append('N')
		exec("nomes2.append('x_%s')" % (i))
		profit2.append(c[i]*l[i])
		types2.append('N')
		exec("nomes3.append('x_%s')" % (i))
		profit3.append(c[i]*l[i])
		types3.append('N')

	for j in range(2):
		exec("nomes.append('z_%s')" % (j))
		profit.append(multa[j])
		types.append('S')
		exec("nomes2.append('z_%s')" % (j))
		profit2.append(-multa[j])
		types2.append('S')
		exec("nomes3.append('z_%s')" % (j))
		profit3.append(-multa[j])
		types3.append('S')
					 
		exec("nomes.append('y_%s')" % (j))
		profit.append(0)
		types.append('S')
		exec("nomes2.append('y_%s')" % (j))
		profit2.append(0)
		types2.append('S')
		exec("nomes3.append('y_%s')" % (j))
		profit3.append(0)
		types3.append('S')



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

	expr3 = []
	coeficientes3 = []
	senses3 = []
	lista_aux3 = []
	lista_geral3 = []
	rhs3 = []
	names3= []
	pp = 0
	#demanda
	for i in range(num_produtos):
		exec("expr.append('x_%s')" % (i))
		coeficientes.append(c[i] * l[i])
		exec("expr2.append('x_%s')" % (i))
		coeficientes2.append(c[i])
	for j in range(2):
		exec("expr.append('z_%s')" % (j))
		coeficientes.append(-multa[j])
		exec("expr2.append('z_%s')" % (j))
		coeficientes2.append(multa[j])
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


	# In[13]:


	for j in range(2):
		expr = []
		coeficientes = []
		for i in range(num_produtos):
			exec("expr.append('x_%s')" % (i))
			coeficientes.append(h[i][j])
		exec("expr.append('y_%s')" % (j))
		coeficientes.append(-1)
		exec("expr.append('z_%s')" % (j))
		coeficientes.append(-1)
		senses.append('E')
		rhs.append(0)
		exec("names.append('c_%s')" % (pp))
		lista_aux = [expr,coeficientes]
		lista_geral += [lista_aux]
		
		
		expr2 = []
		coeficientes2 = []
		for i in range(num_produtos):
			exec("expr2.append('x_%s')" % (i))
			coeficientes2.append(h[i][j])
		exec("expr2.append('y_%s')" % (j))
		coeficientes2.append(-1)
		exec("expr2.append('z_%s')" % (j))
		coeficientes2.append(-1)
		senses2.append('E')
		rhs2.append(0)
		exec("names2.append('c_%s')" % (pp))
		lista_aux2 = [expr2,coeficientes2]
		lista_geral2 += [lista_aux2]
		
		
		expr3 = []
		coeficientes3 = []
		for i in range(num_produtos):
			exec("expr3.append('x_%s')" % (i))
			coeficientes3.append(h[i][j])
		exec("expr3.append('y_%s')" % (j))
		coeficientes3.append(-1)
		exec("expr3.append('z_%s')" % (j))
		coeficientes3.append(-1)
		senses3.append('E')
		rhs3.append(0)
		exec("names3.append('c_%s')" % (pp))
		lista_aux3 = [expr3,coeficientes3]
		lista_geral3 += [lista_aux3]
		pp += 1
		


	# In[14]:


	for j in range(2):
		expr = []
		coeficientes = []
		exec("expr.append('y_%s')" % (j))
		coeficientes.append(1)
		senses.append('L')
		rhs.append(capacidade[j])
		exec("names.append('c_%s')" % (pp))
		lista_aux = [expr,coeficientes]
		lista_geral += [lista_aux]
		pp += 1    
		expr = []
		coeficientes = []
		exec("expr.append('z_%s')" % (j))
		coeficientes.append(1)
		senses.append('L')
		rhs.append(extras[j])
		exec("names.append('c_%s')" % (pp))
		lista_aux = [expr,coeficientes]
		lista_geral += [lista_aux]
		pp += 1
		
		expr2 = []
		coeficientes2 = []
		exec("expr2.append('y_%s')" % (j))
		coeficientes2.append(1)
		senses2.append('L')
		rhs2.append(capacidade[j])
		exec("names2.append('c_%s')" % (pp))
		lista_aux2 = [expr2,coeficientes2]
		lista_geral2 += [lista_aux2]
		pp += 1    
		expr2 = []
		coeficientes2 = []
		exec("expr2.append('z_%s')" % (j))
		coeficientes2.append(1)
		senses2.append('L')
		rhs2.append(extras[j])
		exec("names2.append('c_%s')" % (pp))
		lista_aux2 = [expr2,coeficientes2]
		lista_geral2 += [lista_aux2]
		pp += 1
		
		
		expr3 = []
		coeficientes3 = []
		exec("expr3.append('y_%s')" % (j))
		coeficientes3.append(1)
		senses3.append('L')
		rhs3.append(capacidade[j])
		exec("names3.append('c_%s')" % (pp))
		lista_aux3 = [expr3,coeficientes3]
		lista_geral3 += [lista_aux3]
		pp += 1    
		expr3 = []
		coeficientes3 = []
		exec("expr3.append('z_%s')" % (j))
		coeficientes3.append(1)
		senses3.append('L')
		rhs3.append(extras[j])
		exec("names3.append('c_%s')" % (pp))
		lista_aux3 = [expr3,coeficientes3]
		lista_geral3 += [lista_aux3]
		pp += 1


	# In[15]:


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
		
		
		
		expr3 = []
		coeficientes3 = []
		exec("expr3.append('x_%s')" % (i))
		coeficientes3.append(1)
		senses3.append('L')
		rhs3.append(d[i]*(1+p[i]))
		exec("names3.append('c_%s')" % (pp))
		lista_aux3 = [expr3,coeficientes3]
		lista_geral3 += [lista_aux3]
		pp += 1
		# Demanda minima
		expr3 = []
		coeficientes3 = []
		exec("expr3.append('x_%s')" % (i))
		coeficientes3.append(1)
		senses3.append('G')
		rhs3.append(d[i]*(1-p[i]))
		exec("names3.append('c_%s')" % (pp))
		lista_aux3 = [expr3,coeficientes3]
		lista_geral3 += [lista_aux3]
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

		ii = 2
		index = 0
		jj = 0
		total_lucros = 0
		# PRINT X
		for i in range(num_produtos):
			Sheet1.range('H{}'.format(ii)).value = row[index]
			total_lucros += row[index] *c[jj]*l[jj]
			ii += 1
			index += 1
			jj += 1
		#PRINT Z[I] E Y[I+1]
		valor_final_multa = 0
		for j in range(2):
			valor_final_multa += row[index] * multa[j]
			index += 2
		Sheet1.range('H15').value = total_lucros - valor_final_multa
		Sheet1.range('I14').value = valor_final_multa
		Sheet1.range('N1').value = ''
		# print(row)
	except CplexError as exc:
		Sheet1.range('N1').value = 'Não foi encontrada solução viável'


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

		index = 0
		# PRINT X
		for i in range(num_produtos):
			Sheet1.range('J{}'.format(ii)).value = row[index]
			total_custos += row[index] *c[jj]
			ii += 1
			index += 1
			jj += 1
		#PRINT Z[I] E Y[I+1]
		valor_final_multa = 0
		for j in range(2):
			valor_final_multa += row[index] * multa[j]
			index += 2
		Sheet1.range('J16').value = total_custos
		Sheet1.range('K15').value = valor_final_multa
		Sheet1.range('N2').value = ''
		# print(row)
	except CplexError as exc:
		Sheet1.range('N2').value = 'Não foi encontrada solução viável'


	try:
		# print(names)
		prob3 = cplex.Cplex()
		prob3.objective.set_sense(prob3.objective.sense.maximize)
		prob3.variables.add(obj = profit2,
					types = types2,
					names = nomes2)

		prob3.linear_constraints.add(lin_expr = lista_geral3,
							senses = senses3,
							rhs = rhs3,
							names = names3)

		# prob.set_log_stream(None)
		# prob.set_error_stream(None)
		# prob.set_warning_stream(None)
		# prob.set_results_stream(None)
		cellset = {}
		# prob.parameters.timelimit.set(60)
		prob3.solve()
		
		row = prob3.solution.get_values()
		index = 0
		total_custos = 0
		ii = 2
		jj = 0

		# PRINT X
		for i in range(num_produtos):
			Sheet1.range('L{}'.format(ii)).value = row[index]
			total_custos += i *c[jj]
			ii += 1
			index += 1
			jj += 1
		#PRINT Z[I] E Y[I+1]
		valor_final_multa = 0
		for j in range(2):
			valor_final_multa += row[index] * multa[j]
			index += 2

		Sheet1.range('M16').value = valor_final_multa
		Sheet1.range('N3').value = ''
		# print(row)
	except CplexError as exc:
		Sheet1.range('N3').value ='Não foi encontrada solução viável'