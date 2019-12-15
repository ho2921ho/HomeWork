Data_inflation = read.csv('C:/GitHub/HomeWork/Time_series/Data_inflation.csv')

xt = Data_inflation$WTI.현물유가등락률[1:288]
xt_1 = Data_inflation$WTI.현물유가등락률[2:289]

yt = Data_inflation$근원인플레이션율[1:288]
yt_1 = Data_inflation$근원인플레이션율[2:289]

reg_fit <- lm(yt~yt_1+xt_1)
summary(reg_fit)

rm(list=ls())
lm.bayes <- function(yt,yt_1,xt_1,tau.b0,tau.b1, tau.b2, beta0=0.001, beta1=0.001, beta2 = 0.001, niter=5000){
  n <- length(yt)
  b0 <- 0.109676
  b1 <- 0.975811 
  b2 <- -0.001813
  tau <- 1
  result <- matrix(nrow=niter, ncol=4)
  for (i in 1:niter){
    beta0 <- rnorm(0.5, mean=(tau/(n*tau+tau.b0))*sum(yt-(b1*yt_1+b2*xt_1)), sd=0.25/sqrt(n*tau+tau.b0))
    beta1 <- rnorm(0.5, mean= (tau*sum((yt-b0*yt_1))/tau*sum(yt_1^2)+tau.b1) ,sd=0.25/sqrt(tau*sum(yt_1^2)+tau.b1))
    beta2 <- rnorm(0, mean=(tau*sum((yt-b0*xt_1))/tau*sum(xt_1^2)+tau.b2),sd=1/sqrt(tau*sum(xt_1^2)+tau.b2))
    
    tau <- rgamma(1, shape=beta0+n/2, rate=beta1+0.5*sum(yt-b0-b1*yt_1)^2)
    
    result[i, ] <- c(b0, b1,b2, tau)
  } 
  result
}

beta.lm <- lm.bayes(yt = yt,yt_1 = yt_1 , xt_1 = xt_1, tau.b0 = 0.001, tau.b1 = 0.001, tau.b2 = 0.001, niter=10000)

beta.lm = beta.lm[-(1:1000),]

colSums(beta.lm)/9000
