#!/bin/python
#-*-coding:utf8-*-
import sys
import re

mappings=[('__n',(
	('ma>+pos<adj','A',1,None),
	('ma>+pos<adj','s',2,None),
	('ma>+pos<adj','p',3,None),
	('ma>+pos<adj','n',7,None),
	('mi>+pos<adj','A',1,None),
	('mi>+pos<adj','s',2,None),
	('mi>+pos<adj','p',3,None),
	('mi>+pos<adj','n',7,None),
	('nt>+pos<adj','A',1,None),
	('nt>+pos<adj','s',2,None),
	('nt>+pos<adj','p',3,None),
	('nt>+pos<adj','n',7,None),
	('f>+pos<adj','A',1,None),
	('f>+pos<adj','s',2,None),
	('f>+pos<adj','p',3,None),
	('f>+pos<adj','n',7,None),
	('f','f',4,lambda x:x[0]=='A'),
	('nt','n',4,lambda x:x[0]=='A'),
	('mi','m',4,lambda x:x[0]=='A'),
	('ma','m',4,lambda x:x[0]=='A'),
	('sg','s',5,lambda x:x[0]=='A'),
	('pl','p',5,lambda x:x[0]=='A'),
	('nom','n',6,lambda x:x[0]=='A'),
	('gen','g',6,lambda x:x[0]=='A'),
	('dat','d',6,lambda x:x[0]=='A'),
	('acc','a',6,lambda x:x[0]=='A'),
	('voc','v',6,lambda x:x[0]=='A'),
	('loc','l',6,lambda x:x[0]=='A'),
	('ins','i',6,lambda x:x[0]=='A'),
	('np','N',1,lambda x:x[0]==' ',),
	('n','N',1,lambda x:x[0]==' ',),
	('np','p',2,lambda x:x[0]=='N'),
	('n','c',2,lambda x:x[0]=='N'),
	('f','f',3,lambda x:x[0]=='N'),
	('nt','n',3,lambda x:x[0]=='N'),
	('mi','m',3,lambda x:x[0]=='N'),
	('ma','m',3,lambda x:x[0]=='N'),
	('sg','s',4,lambda x:x[0]=='N'),
	('pl','p',4,lambda x:x[0]=='N'),
	('nom','n',5,lambda x:x[0]=='N'),
	('gen','g',5,lambda x:x[0]=='N'),
	('dat','d',5,lambda x:x[0]=='N'),
	('acc','a',5,lambda x:x[0]=='N'),
	('voc','v',5,lambda x:x[0]=='N'),
	('loc','l',5,lambda x:x[0]=='N'),
	('ins','i',5,lambda x:x[0]=='N'),
	('mi','n',6,lambda x: x[2:5]=='msa' and x[0]=='N'),
	('ma','y',6,lambda x: x[2:5]=='msa' and x[0]=='N')
)),
('__np',(
	('ma>+pos<adj','A',1,None),
	('ma>+pos<adj','s',2,None),
	('ma>+pos<adj','p',3,None),
	('ma>+pos<adj','n',7,None),
	('mi>+pos<adj','A',1,None),
	('mi>+pos<adj','s',2,None),
	('mi>+pos<adj','p',3,None),
	('mi>+pos<adj','n',7,None),
	('nt>+pos<adj','A',1,None),
	('nt>+pos<adj','s',2,None),
	('nt>+pos<adj','p',3,None),
	('nt>+pos<adj','n',7,None),
	('f>+pos<adj','A',1,None),
	('f>+pos<adj','s',2,None),
	('f>+pos<adj','p',3,None),
	('f>+pos<adj','n',7,None),
	('f','f',4,lambda x:x[0]=='A'),
	('nt','n',4,lambda x:x[0]=='A'),
	('mi','m',4,lambda x:x[0]=='A'),
	('ma','m',4,lambda x:x[0]=='A'),
	('sg','s',5,lambda x:x[0]=='A'),
	('pl','p',5,lambda x:x[0]=='A'),
	('nom','n',6,lambda x:x[0]=='A'),
	('gen','g',6,lambda x:x[0]=='A'),
	('dat','d',6,lambda x:x[0]=='A'),
	('acc','a',6,lambda x:x[0]=='A'),
	('voc','v',6,lambda x:x[0]=='A'),
	('loc','l',6,lambda x:x[0]=='A'),
	('ins','i',6,lambda x:x[0]=='A'),
	('np','N',1,lambda x:x[0]==' ',),
	('np','p',2,lambda x:x[0]=='N'),
	('f','f',3,lambda x:x[0]=='N'),
	('nt','n',3,lambda x:x[0]=='N'),
	('mi','m',3,lambda x:x[0]=='N'),
	('ma','m',3,lambda x:x[0]=='N'),
	('sg','s',4,lambda x:x[0]=='N'),
	('pl','p',4,lambda x:x[0]=='N'),
	('nom','n',5,lambda x:x[0]=='N'),
	('gen','g',5,lambda x:x[0]=='N'),
	('dat','d',5,lambda x:x[0]=='N'),
	('acc','a',5,lambda x:x[0]=='N'),
	('voc','v',5,lambda x:x[0]=='N'),
	('loc','l',5,lambda x:x[0]=='N'),
	('ins','i',5,lambda x:x[0]=='N'),
	('mi','n',6,lambda x: x[2:5]=='msa' and x[0]=='N'),
	('ma','y',6,lambda x: x[2:5]=='msa' and x[0]=='N')
)),('__adj',(
	('adj','A',1,None),
	('adj','g',2,None),
	('pst','p',3,lambda x:x[0]=='A'),
	('comp','c',3,lambda x:x[0]=='A'),
	('sup','s',3,lambda x:x[0]=='A'),
	('ssup','p',3,lambda x:x[0]=='A'), 
	('f','f',4,None),
	('nt','n',4,None),
	('mi','m',4,None),
	('ma','m',4,None),
	('sg','s',5,None),
	('pl','p',5,None),
	('nom','n',6,None),
	('gen','g',6,None),
	('dat','d',6,None),
	('acc','a',6,None),
	('voc','v',6,None),
	('loc','l',6,None),
	('ins','i',6,None),	
	('ind','n',7,None),
	('def','y',7, None),
	('mi','n',8,lambda x: x[3:6]=='msa'),
	('ma','y',8,lambda x: x[3:6]=='msa'),
	('adv','R',1,None),
	('adv','g',2,None),
	('pst','p',3,lambda x:x[0]=='R'),
	('comp','c',3,lambda x:x[0]=='R'),
	('sup','s',3,lambda x:x[0]=='R'),
	('ssup','p',3,lambda x:x[0]=='R')
)),
('possesive__sfx__adj',(
	(None,'A',1,None),
	(None,'s',2,None),
	('f','f',4,None),
	('nt','n',4,None),
	('mi','m',4,None),
	('ma','m',4,None),
	('sg','s',5,None),
	('pl','p',5,None),
	('nom','n',6,None),
	('gen','g',6,None),
	('dat','d',6,None),
	('acc','a',6,None),
	('voc','v',6,None),
	('loc','l',6,None),
	('ins','i',6,None),	
	
	('mi','n',8,lambda x: x[3:6]=='msa'),
	('ma','y',8,lambda x: x[3:6]=='msa')
)),

('__adv',(
	(None,'R',1,None),
	(None,'g',2,None),
	('pst','p',3,None),
	('comp','c',3,None),
	('sup','s',3,None),
	(None,'p',3,lambda x:x[2]==' ')
)),	
	#Zapis: V[ma][rnmaifp][123][sp][mfn][ny]
	# "f" za futur od "biti" (futII)u __vbser. "f" za futur od "htjeti" je "futI" u __vbmod 
	# pazi: "pp" ima pardef n="pp__adj__sfx"
	# kod vbmod sam na poziciju 2 stavila "o" (oznaku koju nemamo) jer je modalni (htjeti). On je pomoćni SAMO u prezentskim enklitičkim oblicima kad tvori futurI. Ovo treba riješiti
	# nenaglašeni oblici htjeti (vbmod)i biti (vbser) bilježi se atributom n="clt".  Treba li i nama to?
	# Apertium razlikuje i glagol imati (n="vbhaver") koji uz sebe ima atribute n="iv"- intransitive te n="tv"-transitive
	# Apertium ima definiciju <sdef n="vaux" c="Auxilliary verb"/> ali je nigdje ne koristi
	
('__vblex',(
	('adv','R',1,None),
	('pprs','s',2,lambda x:x[0]=='R'),
	('adv','p',2,lambda x:x[1]==' '),
	('vblex','V',1,lambda x:x[0]==' '),
	('vblex','m',2,lambda x:x[0]=='V'),
	('pres','r',3,lambda x:x[0]=='V'),
	('inf','n',3,lambda x:x[0]=='V'),
	('imp','m',3,lambda x:x[0]=='V'),
	('aor','a',3,lambda x:x[0]=='V'),
	('pii','i',3,lambda x:x[0]=='V'),
	('lp','p',3,lambda x:x[0]=='V'),
	('p1','1',4,lambda x:x[0]=='V'),
	('p2','2',4,lambda x:x[0]=='V'),
	('p3','3',4,lambda x:x[0]=='V'),
	('sg','s',5,lambda x:x[0]=='V'),
	('pl','p',5,lambda x:x[0]=='V'),
	('m','m',6,lambda x:x[0]=='V'),
	('f','f',6,lambda x:x[0]=='V'),
	('nt','n',6,lambda x:x[0]=='V'),
	('neg','n',7,lambda x:x[0]=='V'),
	('pp','A',1,None),
	('pp','p',2,None),
	('pp','p',3,None),
	('mi','m',4,lambda x:x[0]=='A'),
	('ma','m',4,lambda x:x[0]=='A'),
	('f','f',4,lambda x:x[0]=='A'),
	('nt','n',4,lambda x:x[0]=='A'),
	('sg','s',5,lambda x:x[0]=='A'),
	('pl','p',5,lambda x:x[0]=='A'),
	('nom','n',6,lambda x:x[0]=='A'),
	('gen','g',6,lambda x:x[0]=='A'),
	('dat','d',6,lambda x:x[0]=='A'),
	('acc','a',6,lambda x:x[0]=='A'),
	('voc','v',6,lambda x:x[0]=='A'),
	('loc','l',6,lambda x:x[0]=='A'),
	('ins','i',6,lambda x:x[0]=='A'),
	('ind','n',7,lambda x:x[0]=='A'),
	('def','y',7,lambda x:x[0]=='A'),
	
))]

filters={'__vblex':re.compile(r'\s.+?\t')}#'__np':re.compile(r'mi>\+pos<adj')}#,'__adj':re.compile(r' ssup ')}

for line in sys.stdin:
	tag=[' ']*20
	if line.startswith('#'):
		par,lem=line.strip('#\n').split('\t')
		for mapping in mappings:
			if par.endswith(mapping[0]):
				map=mapping[1]
				filter=filters.get(mapping[0])
				break
		if map==None:
			sys.stderr.write('\nUnknown paradigm! '+par+'\n\n')
			sys.exit(1)
		sys.stdout.write('\n'+par+'\t'+lem+'\n')
	elif line.startswith('\n'):
		par,lem,map=None,None,None
	else:
		if filter is not None:
			if filter.search(line) is not None:
				continue
		tok,tags=line.strip().split('\t')
		tags=set(tags.split())
		for pre,let,pos,fun in map:
			if pre is not None: # check prerequisite (Apertium tag)
				if pre not in tags:
					continue
			if fun is not None: # check additional constraint (part of MTE tag) 
				if not fun(''.join(tag)):
					continue
			tag[int(pos)-1]=let
		sys.stdout.write(tok+'\t'+''.join(tag).strip().replace(' ','-')+'\n')
