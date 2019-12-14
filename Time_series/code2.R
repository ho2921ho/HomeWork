Data_inflation = read.csv('C:/GitHub/HomeWork/Time_series/Data_inflation.csv')

xt = Data_inflation$WTI.현물유가등락률[1:288]
xt_1 = Data_inflation$WTI.현물유가등락률[2:289]

yt = Data_inflation$근원인플레이션율[1:288]
yt_1 = Data_inflation$근원인플레이션율[2:289]

rm(list=ls())
lm.bayes <- function(y,x,tau.a,tau.b, alpha=0.001, beta=0.001, niter=5000){
  n <- length(y)
  a <- 83.419
  b <- 10.210
  tau <- 1
  result <- matrix(nrow=niter, ncol=3)
  for (i in 1:niter){
    a <- rnorm(1, mean=(tau/(n*tau+tau.a))*sum(y-b*x), sd=1/sqrt(n*tau+tau.a))
    b <- rnorm(1, mean=(tau*sum((y-a*x))/tau*sum(x^2)+tau.b),
               sd=1/sqrt(tau*sum(x^2)+tau.b))
    tau <- rgamma(1, shape=alpha+n/2, rate=beta+0.5*sum(y-a-b*x)^2)
    result[i, ] <- c(a, b, tau)
  } ## 숙제로 나온 부분. 
  result
}