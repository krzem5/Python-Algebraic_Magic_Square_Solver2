import re



def split_multiple(s,dl):
	return re.split("|".join(map(re.escape,dl)),s)



def log(sq):
	ml=0
	for r in sq:
		for c in r:
			if (c is None):
				continue
			ml=max(ml,len(str(c)))
	ml+=2
	s="\n"
	for r in sq:
		for c in r:
			s+=str(c if c!=None else "").center(ml," ")+"|"
		s=s[:len(s)-1]+"\n"+"-"*(len(sq[0])*ml+len(sq[0])-1)+"\n"
	s=s[:len(s)-1-(len(sq[0])*ml+len(sq[0])-1)-1]+"\n"
	return s



def solve(sq,log_steps=False):
	def alg_to_dict(seq):
		alg={}
		seq=str(seq).replace("--","+").replace("-","+-").split("+")
		for i in seq:
			neg="-" in i
			i=i.replace("-","")
			if (i==""):
				continue
			l=[]
			for c in i:
				if (c.isalpha()):
					l.append(c)
			if (len(l)==0):
				alg["num"]=(-1 if neg==True else 1)*int(i)
				continue
			l.sort()
			i=split_multiple(i,l)
			l="".join(l)
			t=1
			for n in i:
				if (n==""):continue
				t*=int(n)
			alg[l]=(-1 if neg==True else 1)*t
		return alg
	def dict_to_alg(d):
		alg=""
		for k in d.keys():
			if (d[k]==0):continue
			alg+=("" if (d[k]==1 and k!="num") else str(d[k]))+(k if k!="num" else "")+"+"
		alg=alg[:len(alg)-1].replace("+-","-")
		if (alg==""):
			alg="0"
		try:
			alg=int(alg)
		except ValueError:
			pass
		return alg
	def conv_alg(sml):
		total={}
		for i in sml:
			i=alg_to_dict(i)
			for k in i.keys():
				if (k in total.keys()):
					total[k]+=i[k]
				else:
					total[k]=i[k]
		return total
	def sub_alg(a,b):
		rem={}
		for k in a.keys():
			rem[k]=a[k]
		for k in b.keys():
			if (k in rem.keys()):
				rem[k]-=b[k]
			else:
				rem[k]=-b[k]
		return rem
	def floor_div_alg(a,d):
		b={}
		for k in a:
			b[k]=a[k]//d
		return b
	def equal_alg(a,b):
		for k in a:
			if (k=="num" and a[k]==0):
				continue
			if (k not in b.keys() or b[k]!=a[k]):
				return False
		for k in b:
			if (k=="num" and b[k]==0):
				continue
			if (k not in a.keys() or a[k]!=b[k]):
				return False
		return True
	total={}
	left=0
	w=len(sq[0])
	h=len(sq)
	ot=[]
	for r in sq:
		for c in r:
			if (c is None):
				left+=1
			else:
				ot.append(c)
	ot=conv_alg(ot)
	for i in range(0,h):
		sml=[]
		s=True
		for j in range(0,w):
			if (sq[i][j] is None):
				s=False
				break
			else:
				sml.append(sq[i][j])
		if (s==True):
			total=conv_alg(sml)
			break
	if (len(total.keys())==0):
		for i in range(0,h):
			sml=[]
			s=True
			for j in range(0,w):
				if (sq[j][i] is None):
					s=False
					break
				else:
					sml.append(sq[j][i])
			if (s==True):
				total=conv_alg(sml)
				break
	if (len(total.keys())==0):
		sml=[]
		s=True
		for i in range(0,min(w,h)):
			if (sq[i][i] is None):
				s=False
				break
			else:
				sml.append(sq[i][i])
		if (s==True):
			total=conv_alg(sml)
	if (len(total.keys())==0):
		sml=[]
		s=True
		for i in range(0,min(w,h)):
			if (sq[i][min(w,h)-1-i] is None):
				s=False
				break
			else:
				sml.append(sq[i][min(w,h)-1-i])
		if (s==True):
			total=conv_alg(sml)
	if (len(total.keys())==0):
		total=ot
		total=floor_div_alg(total,2)
		print(total)
	while (True):
		if (log_steps==True):
			log(sq)
		if (left==0):
			break
		state=False
		for i in range(0,h):
			cnt=0
			sml=[]
			off=0
			for j in range(0,w):
				if (sq[i][j] is None):
					cnt+=1
					off=j
				else:
					sml.append(sq[i][j])
			if (cnt==1):
				sq[i][off]=dict_to_alg(sub_alg(total,conv_alg(sml)))
				state=True
				left-=1
				break
		if (state==True):
			continue
		for i in range(0,h):
			cnt=0
			sml=[]
			off=0
			for j in range(0,w):
				if (sq[j][i] is None):
					cnt+=1
					off=j
				else:
					sml.append(sq[j][i])
			if (cnt==1):
				sq[off][i]=dict_to_alg(sub_alg(total,conv_alg(sml)))
				state=True
				left-=1
				break
		if (state==True):
			continue
		cnt=0
		sml=[]
		off=0
		for i in range(0,min(w,h)):
			if (sq[i][i] is None):
				cnt+=1
				off=i
			else:
				sml.append(sq[i][i])
		if (cnt==1):
			sq[off][off]=dict_to_alg(sub_alg(total,conv_alg(sml)))
			state=True
			left-=1
		if (state==True):
			continue
		cnt=0
		sml=[]
		off=0
		for i in range(0,min(w,h)):
			if (sq[i][min(w,h)-1-i] is None):
				cnt+=1
				off=i
			else:
				sml.append(sq[i][min(w,h)-1-i])
		if (cnt==1):
			sq[off][min(w,h)-1-off]=dict_to_alg(sub_alg(total,conv_alg(sml)))
			state=True
			left-=1
		if (state==True):
			continue
		return (False,"Unable to put-in all the numbers")
	for i in range(0,h):
		sml=[]
		for j in range(0,w):
			sml.append(sq[i][j])
		if (equal_alg(total,conv_alg(sml))==False):
			return (False,"Values do not match the total")
	for i in range(0,h):
		sml=[]
		for j in range(0,w):
			sml.append(sq[j][i])
		if (equal_alg(total,conv_alg(sml))==False):
			return (False,"Values do not match the total")
	sml=[]
	for i in range(0,min(w,h)):
		sml.append(sq[i][i])
	if (equal_alg(total,conv_alg(sml))==False):
		return (False,"Values do not match the total")
	sml=[]
	for i in range(0,min(w,h)):
		sml.append(sq[i][min(w,h)-1-i])
	if (equal_alg(total,conv_alg(sml))==False):
		return (False,"Values do not match the total")
	return (True,sq)



if __name__=="__main__":
	sq=[["5p+2",0,"4p+1"],["2p",None,None],[None,None,None]]
	# sq=[["n","2m",None],["2m+2n",None,None],["m",None,None]]
	# sq=[["4a+b","2c",None],[None,"3a+b+c",None],[None,None,"2a+b+2c"]]
	print(log(sq))
	o=solve(sq,log_steps=False)
	if (o[0]==False):
		print(o[1])
	else:
		print(log(o[1]))
