import os, sys

os.umask(0000)

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import glob
import numpy as np
import pickle
import subprocess
import pdb
import db
from time import time, sleep
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', dest='s', required=True)
parser.add_argument('-c', dest='c', required=True)
ins = parser.parse_args()

#initialize database session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://subptf:p33d$kyy@scidb2.nersc.gov:5432/subptf'
datb = SQLAlchemy(app)
with open('/project/projectdirs/deepsky/src/scripts/rb_classifier/arff.header', 'r') as f:
    arffhead = f.read()

#----------------------------------------------------------------------#
# set environment variables
#----------------------------------------------------------------------#

os.environ['JAVA_HOME'] = '/project/projectdirs/sgn/software/java-1.6.0_12/jdk1.6.0_12'
os.environ['CLASSPATH'] = '/project/projectdirs/sgn/software/usg/weka/weka-3-5-7/weka.jar'

#----------------------------------------------------------------------#
# methods for extracting features
#----------------------------------------------------------------------#

def init(args):
    global num_done
    num_done = args

def pos_sub(ca, sa):
    return ca['pos_sub']

def flux_ratio(ca, sa):
    return ca['f_aper'] / ca['flux_aper'] if ca['flux_aper'] != 0 else '?'

def ellipticity(ca, sa):
    return 1 - (ca['b_image'] / ca['a_image']) if ca['a_image'] != 0 else '?'

def ellipticity_ref(ca, sa):
    return 1 - (ca['b_ref'] / ca['a_ref']) if ca['a_ref'] != 0 else '?'

def nn_dist_renorm(ca, sa):
    return 100000.0 * ca['nn_dist']

def magdiff(ca, sa):
    return ca['mag'] - ca['mag_ref']

def maglim(ca, sa):
    return 't' if ca['mag_ref'] < 1E-29 else 'f'

def sigflux(ca, sa):
    return ca['flux'] / ca['flux_err'] if ca['flux_err'] != 0 else '?'

def seeing_ratio(ca, sa):
    return sa['seeing_new']/sa['seeing_ref'] if sa['seeing_ref'] != 0 else '?'

def mag_from_limit(ca, sa):
    return sa['lmt_mg_ref'] - ca['mag']

def normalized_fwhm(ca, sa):
    return ca['fwhm']/sa['seeing_new'] if sa['seeing_new'] != 0 else '?'

def normalized_fwhm_ref(ca, sa):
    return ca['fwhm_ref']/sa['seeing_ref'] if sa['seeing_ref'] != 0 else '?'

def good_cand_density(ca, sa):
    return sa['objs_saved'] / sa['good_pix_area'] if sa['good_pix_area'] != 0 else '?'

def min_dist_to_edge_in_new(ca, sa):
	return min([min([2048.0-ca['x_sub'], ca['x_sub']]), min([4096.0-ca['y_sub'], ca['y_sub']])])

def mag(ca, sa):
	return ca['mag']

def mag_err(ca, sa):
	return ca['mag_err']

def a_image(ca, sa):
	return ca['a_image']

def b_image(ca, sa):
	return ca['b_image']

def fwhm(ca, sa):
	return ca['fwhm']

def flag(ca, sa):
	return ca['flag']

def mag_ref(ca, sa):
	return ca['mag_ref']

def mag_ref_err(ca, sa):
	return ca['mag_ref_err']

def a_ref(ca, sa):
	return ca['a_ref']

def b_ref(ca, sa):
	return ca['b_ref']

def n2sig3(ca, sa):
	return ca['n2sig3']

def n3sig3(ca, sa):
	return ca['n2sig3']

def n2sig5(ca, sa):
	return ca['n2sig5']

def n3sig5(ca, sa):
	return ca['n3sig5']

def nmask(ca, sa):
	return ca['nmask']

def split_seq(l, np):
    step_size = len(l) / np
    newseq = []
    for i in range(np):
        if i != np-1:
            newseq.append(l[i * step_size : (i + 1) * step_size])
        else:
            newseq.append(l[i * step_size:])
    return newseq

#----------------------------------------------------------------------#
# extract features from loaded files and write to .arff file
#----------------------------------------------------------------------#

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
        
    return d
    
def run_ml_load_db(sub_filename, cand_filename, fakes_version):

    datb = SQLAlchemy(app)

    cand_names = pickle.load(open('/project/projectdirs/deepsky/rates/icecube/eno/cand_names.obj', 'rb'))
    sub_names = pickle.load(open('/project/projectdirs/deepsky/rates/icecube/eno/sub_names.obj', 'rb'))
    
    for cand, sub in [(cand_filename, sub_filename)]:
        sub_root = '/'.join(sub.split('/')[:-1])
        os.chdir(sub_root)
        sub_arr = np.genfromtxt(sub, dtype=None, names=sub_names, delimiter='\t', autostrip=True)
        cand_arr = np.genfromtxt(cand, dtype=None, names=cand_names, delimiter='\t', autostrip=True)

        prefilled = len([row for row in datb.session.query(db.Subtraction).filter(db.Subtraction.filename == str(sub_arr['filename'])).filter(db.Subtraction.fakes_version == fakes_version)]) > 0
        
        if prefilled:
            print 'WARNING: subtraction {0} already has an entry in the database with fakes_version = {1}'.format(str(sub_arr['filename']), fakes_version)
            with open('WARNING.{0}.log'.format(str(sub_arr['filename']).strip()), 'w') as f:
                f.write('Sub To Be Added:\n')

                f.write('{0}\n'.format(dict(zip(sub_arr.dtype.names, sub_arr.tolist()))))
                f.write('Subs already in DB' + '\n')                
                query = datb.session.query(db.Subtraction).filter(db.Subtraction.filename == str(sub_arr['filename'])).filter(db.Subtraction.fakes_version == fakes_version)
                for row in query:
                    f.write('{0}\n'.format(row2dict(row)))
                    
            print 'DETAILS PRINTED TO WARNING.{0}.log. Consider removing these duplicates from the database.'.format(str(sub_arr['filename']).strip())

        try:
                    
            sub_ingest = db.Subtraction(**dict(zip(sub_arr.dtype.names, sub_arr.tolist())))

        except Exception as e:
            print 'zeropoint failed on sub {0}'.format(sub)
            sub_ingest = db.Subtraction(**dict(zip(sub_arr.dtype.names[:-1], sub_arr.tolist()[:-1])))
        
        sub_ingest.fakes_version = fakes_version

        datb.session.add(sub_ingest)
        datb.session.flush()


        if not os.path.exists('{0}/classification'.format(sub_root)): os.mkdir('{0}/classification'.format(sub_root))
    
        with open('{1}/classification/rb_classifier_{0}.arff'.format(sub_ingest.id, sub_root), 'w') as f:
            f.write(arffhead)

            for crow in cand_arr:

                cand_ingest = db.Candidate(**dict(zip(crow.dtype.names, crow.tolist())))
                cand_ingest.sub = sub_ingest
                cand_ingest.is_star = False
                cand_ingest.is_fake = False
                datb.session.add(cand_ingest)
                datb.session.flush()

                args = crow, sub_arr
                fstring = ','.join(['{' + str(i) + '}' for i in range(30)]).format(
                    mag(*args), 
                    mag_err(*args), 
                    a_image(*args), 
                    b_image(*args), 
                    fwhm(*args),
                    flag(*args), 
                    mag_ref(*args), 
                    mag_ref_err(*args), 
                    a_ref(*args), 
                    b_ref(*args),
                    n2sig3(*args), 
                    n3sig3(*args), 
                    n2sig5(*args), 
                    n3sig5(*args), 
                    nmask(*args),
                    pos_sub(*args), 
                    flux_ratio(*args), 
                    ellipticity(*args), 
                    ellipticity_ref(*args),
                    nn_dist_renorm(*args), 
                    magdiff(*args), 
                    maglim(*args), 
                    sigflux(*args),
                    seeing_ratio(*args), 
                    mag_from_limit(*args), 
                    normalized_fwhm(*args), 
                    normalized_fwhm_ref(*args),
                    good_cand_density(*args), 
                    min_dist_to_edge_in_new(*args), 
                    '?') + '\n'
                f.write(fstring)            

        os.system("/project/projectdirs/sgn/software/java-1.6.0_12/jdk1.6.0_12/bin/java -Xms512m -Xmx1024m weka.classifiers.meta.MetaCost -T {1}/classification/rb_classifier_{0}.arff -l /project/projectdirs/deepsky/lib/rb_classifier/PTFgray-short-weka357.model -p 0 -distribution > {1}/classification/newclass-jb1_{0}.out".format(sub_ingest.id, sub_root))
        
        
        os.system( "/project/projectdirs/deepsky/rates/python/anaconda/bin/python /project/projectdirs/deepsky/rates/icecube/eno/ptf/assemble_classification_results.py -inname {1}/classification/newclass-jb1_{0}.out -oname {1}/classification/PTFgray-all-class-2_{0}.txt".format(sub_ingest.id, sub_root) )
        clf_results = np.loadtxt('{1}/classification/PTFgray-all-class-2_{0}.txt'.format(sub_ingest.id, sub_root))
        query = datb.session.query(db.Candidate).filter(db.Candidate.subtraction_id == sub_ingest.id).order_by(db.Candidate.id)
        for i, c in enumerate(query):
            c.ml_bogus = clf_results[i][0]
            c.ml_suspect = clf_results[i][1]
            c.ml_unclear = clf_results[i][2]
            c.ml_maybe = clf_results[i][3]
            c.ml_real = clf_results[i][4]
            class_arr = ['bogus', 'suspect', 'unclear', 'maybe', 'real']
            class_ = class_arr[np.argmax(clf_results[i][:5])]
            c.ml_class = class_
            c.ml = clf_results[i][1] * 0.15 + clf_results[i][2] * 0.25 + \
                   clf_results[i][3] * 0.5 + clf_results[i][4]
            if 'fake' in sub:
                c.is_fake = True
        datb.session.flush()
        datb.session.commit()
        print 'Successfully ran ML and loaded DB for sub {0}'.format(sub_filename)
    
sub_filename = ins.s
cand_filename = ins.c
fakes_version = int(cand_filename.split('fakesV')[1].split('_')[0])

run_ml_load_db(sub_filename, cand_filename, fakes_version)
