import subprocess

for i in ['2009', '2010', '2011', '2012']:
	for j in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
		for k in ['C00','C01','C02','C04','C05','C06','C07','C08','C09','C10','C11']:
			for l in ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10']:
				#print '{}_{}/{}/{}'.format(i,j,k,l)
				subprocess.call('mkdir -p subs/'+i+'_'+j+'/'+k+'/'+l,shell=True)

f=open('sub_test.txt','r')
for line in f:
	original=line.strip()
	ln=line.split('/')
	name=ln[-1]
	secs=name.split('_')
	dates=secs[0]
	s=list(dates)
	year=s[3]+s[4]+s[5]+s[6]
	month=s[7]+s[8]
	#print '{}_{}'.format(year,month)
	#print dates
	chip=secs[4].split('.')[0]
	version=secs[-1].split('.')[0].split('fakes')[1]
	#print '{}_{}/C{}/{}'.format(year,month,chip,version)
	print 'cp {} subs/{}_{}/C{}/{}'.format(original,year,month,chip,version)
