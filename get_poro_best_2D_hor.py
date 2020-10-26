# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from skimage import data
import numpy as np
import statistics as stat
from skimage import io
import skimage.filters as filters



#sizestr = 'big' # low resolution
#sizestr = 'sm' # high resolution

#noistr = 'pt'
#numnois = 5
#noistr = 'blur'
#numnois = 4

fold = '/Users/mcbeck/Dropbox/HADES/segmentation/data/cropfigs/'
#zbigs = [516, 544, 617, 1253, 1474] 


sizs = ['big', 'sm']
nois = ['pt', 'blur']
numns = [5, 4]

nti=0
for noistr in nois:
    numnois = numns[nti]
    nti=nti+1
    
    for sizestr in sizs:
        zbigs = [0, 9,18,28,37,46,55,64,74,83,92,101,111,120,129,138,147,157,166,175,184,193,203,212,221,230,240,249,258,267,276,286,295,304,313,322,332,341,350,359,368,378,387,396,405,415,424,433,442,451,461,470,479,488,497,507,516,525,534,544,553,562,571,580,590,599,608,617,626,636,645,654,663,672,682,691,700,709,719,728,737,746,755,765,774,783,792,801,811,820,829,838,848,857,866,875,884,894,903,912,921,930,940,949,958,967,976,986,995,1004,1013,1023,1032,1041,1050,1059,1069,1078,1087,1096,1105,1115,1124,1133,1142,1151,1161,1170,1179,1188,1198,1207,1216,1225,1234,1244,1253,1262,1271,1280,1290,1299,1308,1317,1327,1336,1345,1354,1363,1373,1382,1391,1400,1409,1419,1428,1437,1446,1455,1465,1474,1483,1492,1502,1511,1520,1529,1538,1548,1557,1566,1575,1584,1594,1603,1612,1621,1631,1640,1649,1658,1667,1677,1686,1695,1704,1713,1723,1732,1741,1750,1759,1769,1778,1787,1796,1806,1815,1824,1833,1842,1852,1861,1870,1879,1888,1898,1907,1916,1925,1935,1944,1953,1962,1971,1981,1990,1999]
                
        mthr = 29000
        if sizestr=='sm':
            mthr = 28000
        
        txtf = 'output/best_segment_'+noistr+'_'+sizestr+'_hor2D.txt'
        totlines = "z noise method #_correct_frac #_correct_sol mean_acc poro std mean\n"
        for imn in zbigs:
            imstr = str(imn)
            while len(imstr)<4:
                imstr = '0'+imstr
            
            
            # get the original image
            nstr = noistr+'0'
            
            figr = sizestr+'_z'+imstr+'_'+nstr
            nfil = 'wg04'+sizestr+'_'+imstr+'_'+nstr+'.tif'
            print(nfil)
            
            imtrue = io.imread(fold+nfil)
            vals = imtrue.flatten()
            vals = [float(v) for v in vals]
            tsig = stat.stdev(vals)
            tmu = stat.mean(vals)
            
            fractrue = imtrue>tmu
            solidtrue = imtrue<tmu 
            
            fracvol_obs = sum(fractrue.flatten())
            solvol_obs = sum(solidtrue.flatten())
            
            isfractrue = fractrue==True
            issoltrue = fractrue==False
            
            fracnum_obs = sum(isfractrue.flatten())
            solnum_obs = sum(issoltrue.flatten())
            
            ni=0
            while ni<=numnois:
                nstr = noistr+str(ni)
        
                figr = sizestr+'_z'+imstr+'_'+nstr
                nfil = 'wg04'+sizestr+'_'+imstr+'_'+nstr+'.tif'
                print(nfil)
                
                image = io.imread(fold+nfil)
                vals = image.flatten()
                vals = [float(v) for v in vals]
                nsig = stat.stdev(vals)
                nmu = stat.mean(vals)
            
                mi=1
                thr = mthr
                while mi<=3:
                    
                    if mi==1:
                        thr = mthr 
                    elif mi==2:
                        thr = filters.threshold_isodata(image)
                    elif mi==3:
                        thr = filters.threshold_otsu(image)  
                
                    
                    frac = image>thr
                    solid = image<=thr
        
                    correct = frac==fractrue
                    correct = correct.flatten()
                    numcor = np.sum(correct)
                    totvox = len(correct)
                    accfrac = numcor/totvox
                    
                    corsol = solid==solidtrue
                    corsol = corsol.flatten()
                    numsol = np.sum(corsol)
                    accsol = numsol/totvox
                    
                    accur = (numcor+numsol)/(numcor+numsol+(totvox-numcor)+(totvox-numsol))
                    
                    isfracg = frac==True
                    isfrac = isfracg.flatten()
                    fracvol = np.sum(isfrac)
                    issolg = frac==False
                    issol = issolg.flatten()
                    solvol = np.sum(issol)
                    
                    # how many of the fracture voxels are correctly identified?
                    cor = isfracg==isfractrue
                    fraccor = cor[isfracg].flatten()
                    accurfrac = np.sum(fraccor)/fracnum_obs
                    
                    cor = issolg==issoltrue
                    solcor = cor[issolg].flatten()
                    accursol = np.sum(solcor)/solnum_obs
                    
                    #solcor = issolg==issoltrue
                    #numsolcor = np.sum(solcor.flatten())
                    
                    poro = fracvol/(fracvol+solvol)
 
                    fracvol_pred = sum(isfrac)
                    solvol_pred = sum(issol)
        
                    frac_rat = fracvol_pred/fracvol_obs
                    sol_rat = solvol_pred/solvol_obs
                    
                    frmt= "%s %d %d %f %f %f %f %f %f\n" % (imstr, ni, mi, accurfrac, accursol, accur, poro, frac_rat, sol_rat)
        
                    totlines= totlines+frmt
                    
        #            fig, ax = plt.subplots()
        #            ax.imshow(frac)
        #            plt.title(nstr+' '+tits[mi-1]+' m='+str(mi))
        #            plt.xticks([])
        #            plt.yticks([])
        #            plt.show()
                    print(frmt)
                    
                    mi=mi+1
        
                ni=ni+1
           
        
        print(totlines) 
        
        f = open(txtf, "w")
        f.write(totlines)
        f.close()
        
        print(txtf)  
         
