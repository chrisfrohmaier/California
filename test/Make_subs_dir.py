import subprocess

for i in ['2009', '2010', '2011', '2012']:
	for j in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
		for k in ['C00','C01','C02','C04','C05','C06','C07','C08','C09','C10','C11']:
			for l in ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10']:
				#print '{}_{}/{}/{}'.format(i,j,k,l)
				subprocess.call('mkdir -p subs/'+i+'_'+j+'/'+k+'/'+l,shell=True)