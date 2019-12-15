Data_inflation = read.csv('C:/GitHub/HomeWork/Time_series/Data_inflation.csv')

yt_1 = Data_inflation$근원인플레이션율[2:288]
xt_1 = Data_inflation$WTI.현물유가등락률[2:288]
yt = Data_inflation$근원인플레이션율[1:287]

rm(list=ls())
lm.bayes <- function(yt,yt_1,xt_1,tau.b0,tau.b1, tau.b2, beta0=0.001, beta1=0.001, beta2 = 0.001, niter=5000){
  n <- length(yt)
  b0 <- 0.109676
  b1 <- 0.975811 
  b2 <- -0.001813
  tau <- 1
  result <- matrix(nrow=niter, ncol=4)
  for (i in 1:niter){
    beta0 <- rnorm(1, mean=(tau/(n*tau+tau.b0))*sum(yt-(b1*yt_1+b2*xt_1)), sd=1/sqrt(n*tau+tau.b0))
    beta1 <- rnorm(1, mean= (tau*sum((yt-b0*yt_1))/tau*sum(yt_1^2)+tau.b1) ,sd=1/sqrt(tau*sum(yt_1^2)+tau.b1))
    beta2 <- rnorm(1, mean=(tau*sum((yt-b0*xt_1))/tau*sum(xt_1^2)+tau.b2),sd=1/sqrt(tau*sum(xt_1^2)+tau.b2))
    
    tau <- rgamma(1, shape=beta0+n/2, rate=(beta1+beta2)+0.5*sum(yt-b0-b1*yt_1-b2*xt_1)^2)
    result[i, ] <- c(b0, b1,b2, tau)
  } 
  result
}

beta.lm <- lm.bayes(yt = yt,yt_1 = yt_1 , xt_1 = xt_1, tau.b0 = 0.001, tau.b1 = 0.001, tau.b2 = 0.001, niter=10000)

beta.lm = beta.lm[-(1:1000),]

colSums(beta.lm)/9000
plot(cumsum(beta.lm[,1])/(1:9000), type="l", main="b0", ylab="", xlab="")
plot(cumsum(beta.lm[,2])/(1:9000), type="l", main="b1", ylab="", xlab="")
plot(cumsum(beta.lm[,3])/(1:9000), type="l", main="b3", ylab="", xlab="")
plot(cumsum(beta.lm[,4])/(1:9000), type="l", main="tau", ylab="", xlab="")

# 1)
m <- 500; n <- 16; alpha <- 2; beta <- 4; k <- 10
x <- matrix(nrow=m)
x.tmp <- y.tmp <- matrix(nrow=k+1)
betabinom <- function(nsim, size, alpha, beta) {
  pmix <- rbeta(nsim, alpha, beta)
  rbinom(nsim, size, prob=pmix)
}
for (i in 1:m) {
  y.tmp[1] <- rbeta(1,1,1)
  x.tmp[1] <- rbinom(1, n ,y.tmp[1])
  for (j in 2:(k+1)) {
    y.tmp[j] <- rbeta(1, x.tmp[j-1]+alpha, n-x.tmp[j-1]+beta)
    x.tmp[j] <- rbinom(1, n, y.tmp[j])
  }
  x[i] <- x.tmp[k+1]
}
direct <- betabinom(500, 16, 2, 4)
Gibbs <- table(factor(x, levels=c(0:16)))
Direct <- table(factor(direct, levels=c(0:16)))
dataset <- rbind(Gibbs, Direct)
barplot(dataset, beside=TRUE, col=c("black","white"),
        ylim=c(0,80), legend=rownames(dataset))
title(main="Comparison of Two Histograms", font.main=3)