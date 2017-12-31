#calc.py
# Wonderland Model

import numpy as np

#   wonderland(years,Y,K,N,P,tax_rate,Scenario,Noise)
def wonderland(nyears,Y,N,K,P,taw,sc,sf,number_of_iterations):
#   Parameters:
    gamma=0.04
    eta=0.04
    landa=2
    alpha=0.09
    alpha0=10
    alpha1=2.5
    alpha2=2
    beta=0.08
    beta0=40
    beta1=1.375
    theta=15
    delta=1
    epsilon=0.02
    rho=0.2
    omega=0.1
    fi=0.5
    mu=2
    if (sc.lower().strip()=="dream"):
        kappa=1
        xi=0.96
    elif (sc.lower().strip()=="horror"):
        kappa=1
        xi=0.99
    elif (sc.lower().strip()=="escape"):
        kappa=100
        xi=0.99
    elif (sc.lower().strip()=="no_change"):
        #just dummy parameters
        kappa=1
        xi=0.96
    else:
        return "Wrong Scenario!"
# parameters
    y=[0]*(nyears+1);y[0]=Y
    b=[0]*(nyears+1)
    d=[0]*(nyears+1)
    n=[0]*(nyears+1);n[0]=N
    f=[0]*(nyears+1)
    k=[0]*(nyears+1);k[0]=K
    c=[0]*(nyears+1)
    p=[0]*(nyears+1);p[0]=P
    i=[0]*(nyears+1)
    years=[0]*(nyears+1)
#State Form
    if sf==True:
        h=1
    else:
        h=0
    ynoise = np.random.normal(0,1,nyears+1)
    # 0 is the mean of the normal distribution you are choosing from
    # 1 is the standard deviation of the normal distribution
    # 100 is the number of elements you get in array noise
    pnoise = np.random.normal(0,1,nyears+1)


#Calculations
    for t in range(0,nyears):
#Economy
        y0=0.05
        y[t+1]=y[t]*(1+gamma-(gamma+eta)*((1-k[t])**landa)-(y0*taw)/(1-taw))+h*ynoise[t]
        i[t]=y[t]-c[t]
#Population
        b[t]=beta0*(beta1-(2.71828**(beta*i[t]))/(1+2.71828**(beta*i[t])))
        d[t]=alpha0*(alpha1-((2.71828**(alpha*i[t]))/(1+2.71828**(alpha*i[t]))))*(1+alpha2*(1-k[t])**theta)
        n[t+1]=n[t]*(1+(b[t]-d[t])/1000)
#Environment
        f[t]=n[t]*y[t]*p[t]-kappa*(2.71828**(eta*c[t]*n[t]))/(1+2.71828**(eta*c[t]*n[t]))
        if k[t]==0:
            if sc=="horror":
                k[t+1]=0
            if sc=="escape":
                k[t+1]=0.996
        elif k[t]>1 and sc=="escape":
           k[t]=0.005
           k[t+1]=0
        elif k[t]>=0.995959595 and sc=="dream":
            k[t]=0.996
            k[t+1]=0.996

        else:
            k[t+1]=(2.71828**(np.log((k[t])/(1-k[t])))+delta*(k[t]**(rho))-omega*f[t])/(1+(2.71828**(np.log((k[t])/(1-k[t])))+delta*(k[t]**(rho))-omega*f[t]))
        if k[t+1]<=0.5:
            k[t+1]=0

    
        c[t]=fi*((1-k[t])**mu)*y[t]
        p[t+1]=(1-taw)*xi*p[t]+h*pnoise[t]
#years
        years[t]=t
    years[-1]=nyears

    if(sc.lower().strip()=="no_change"):
        y=[1]*len(y)
        n=[1]*len(n)
        k=[1]*len(k)
        p=[1]*len(p)

    return(y,n,k,p,years)
