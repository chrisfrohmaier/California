import subprocess
f=open('sub_list.txt','r')
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
	#print 'cp {} subs/{}_{}/C{}/{}'.format(original,year,month,chip,version)
	subprocess.call('mv '+original+' subs/'+year+'_'+month+'/C'+chip+'/'+version,shell=True)