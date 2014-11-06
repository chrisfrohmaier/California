import psycopg2

con = psycopg2.connect(host='scidb2.nersc.gov', user='subptf', password='p33d$kyy', database='subptf')
cur = con.cursor()
#select ref_filename from subtraction where new_filename like 'PTF200907122424_2_o_42467_00%';
diffem='/project/projectdirs/deepsky/rates/effs/utils/./diffem'
h=open('Global_Subs_List.dat','w')
f=open('all_fits.txt','r')
for line in f:
	ln=line.split('/')
	filen=ln[-1].strip()
	#print filen
	base=filen.split('.')[0]+'%'
	path=ln[0]+'/'+ln[1]+'/'+ln[2]+'/'+ln[3]+'/'+ln[4]+'/'+ln[5]+'/'+ln[6]+'/'+ln[7]+'/'+ln[8]+'/'+ln[9]
	#print path
	#print base
	h.write(str(diffem)+' '+str('ref')+' '+str(filen)+'\n')
	g=open(path+'/sub_list.dat','a')

	cur.execute("SELECT ref_filename from subtraction where new_filename like %s;",(str(base),))
	r=cur.fetchone()
	ref=r[0]
	#print ref
	
	g.write(str(diffem)+' '+str(ref)+' '+str(filen)+'\n')
	g.close()
h.close()