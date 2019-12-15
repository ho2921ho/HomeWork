Data_inflation = read.csv('C:/GitHub/HomeWork/Time_series/Data_inflation.csv')

yt_1 = Data_inflation$근원인플레이션율[2:288]
xt_1 = Data_inflation$WTI.현물유가등락률[2:288]
yt = Data_inflation$근원인플레이션율[1:287]

reg_fit <- lm(yt~yt_1+xt_1)
summary(reg_fit)

library(MASS)
p <- 2
nn <- length(yt)
N <- 10000

X <- cbind(rep(1,nn),yt_1,xt_1) 
beta.hat <- solve(t(X)%*%X)%*%t(X)%*%yt 

s2 <- t(yt)%*%(diag(nn)-X%*%solve(t(X)%*%X)%*%t(X))%*%yt/(nn-p-1) # 

vec.b <- matrix(0,nrow=p+1,ncol=N)

vec.sigma2 <- rep(0,N)

for (m in 1:N){
  r <- rgamma(1,(nn-2)/2,(nn-2)*s2/2)
  vec.sigma2[m] <- 1/r
  b <- mvrnorm(1,beta.hat,solve(t(X)%*%X)/r) # 베타가 정규분포를 따른다고 가정했기에.
  
  vec.b[,m] <- b
}

hist(vec.b[1,],density=-1,yaxt="n",ylab="",xlab="beta0",cex=2,nclass=50,main="",prob = TRUE)
lines(density(vec.b[1,]), col="blue", lwd=2) 
hist(vec.b[2,],density=-1,yaxt="n",ylab="",xlab="beta1",cex=2,nclass=50,main="",prob = TRUE)
lines(density(vec.b[2,]), col="blue", lwd=2) 
hist(vec.b[3,],density=-1,yaxt="n",ylab="",xlab="beta2",cex=2,nclass=50,main="",prob = TRUE)
lines(density(vec.b[3,]), col="blue", lwd=2) 
hist(vec.sigma2,density=-1,yaxt="n",ylab="",xlab="sigma2",cex=2,nclass=50,main="",prob = TRUE)
lines(density(vec.sigma2), col="blue", lwd=2) 
mean(vec.b[1,]); sd(vec.b[1,])
mean(vec.b[2,]); sd(vec.b[2,])
mean(vec.b[3,]); sd(vec.b[2,])
mean(vec.sigma2); sd(vec.sigma2)


# 베이지안의 목표는 무엇? 예측이죠.

vec.new <- rep(0,N)
xnew <- 0.25
for (m in 1:N) {
  r <- rgamma(1,(nn-2)/2,(nn-2)*s2/2)
  b <- mvrnorm(1, beta.hat,solve(t(X)%*%X)/r)
  vec.new[m] <- rnorm(1, mean=b[1]+b[3]*xnew, sd=sqrt(1/r))
}

hist(vec.new,density=-1, yaxt="n",ylab="",xlab="ynew",cex=2,nclass=50,main="")

mean(vec.new)


# Gibbs Sampling # 전제 분포를 제대로 알아야한다. 
# 우리가 가진 데이터를 새로운 데이터로 확장해서 얻겠다. 
# cf) 톰스 샘플링. <- 베이지안을 잘 이용한 샘플링? 요즘 핫하다고 하네요...
# 처음 나오는 샘플은 버리는데, 그 이유는 분포와 결과와 상관없는 가능성이 있어서 , 만번하면 천번은 버린다. 
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

reg_dat <- matrix(c(115.22, 3.69, 135.98, 4.39, 119.34, 4.75, 114.96, 6.03, 187.05,
                    12.47, 243.92, 12.98, 267.43, 14.2, 238.71, 14.76, 295.94, 15.32, 317.78, 16.39, 216,
                    17.35, 240.35, 17.77, 386.57, 17.93, 261.53, 18.43, 249.34, 18.55, 309.87, 18.8,
                    345.89, 18.81, 165.64, 19.04, 196.98, 19.22, 395.26, 19.93, 406.34, 20.13, 171.92,
                    20.33, 303.23, 20.37, 377.04, 20.43, 194.35, 21.45, 213.48, 22.52, 293.87, 22.55,
                    259.61, 22.86, 323.71, 24.2, 275.02, 24.39, 109.71, 24.42, 359.19, 25.2, 201.51,
                    25.5, 460.36, 26.61, 447.76, 26.7, 482.55, 27.14, 438.29, 27.16, 587.66, 28.62,
                    257.95, 29.4, 375.73, 33.4), ncol=2, byrow=T)

beta.lm <- lm.bayes(y=reg_dat[,1], x=reg_dat[,2], tau.a=0.001, tau.b=0.001,
                    niter=10000)

beta.lm = beta.lm[-(1:1000),]

colSums(beta.lm)/9000

plot(cumsum(beta.lm[,1])/(1:9000), type="l", main="a", ylab="", xlab="")
plot(cumsum(beta.lm[,2])/(1:9000), type="l", main="b", ylab="", xlab="")
plot(cumsum(beta.lm[,3])/(1:9000), type="l", main="tau", ylab="", xlab="")

# 베이지안에서 관심은 정확한 값을 추정하는 것이 아니라, 분포를 알아내는 것!!

#Gibbs sampling vs beta-binomial distribution
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


# Estimation of marginal density of X using Gibbs Sampling

rm(list=ls())
m <- 500; n <- 16; alpha <- 2; beta <- 4; k <- 10
x <- y <- matrix(nrow=m)
Gibbs <- Exact <- matrix(nrow=n)
x.tmp <- y.tmp <- matrix(nrow=k+1)
betabinom <- function(x) {
  choose(n, x)*{gamma(alpha+beta)*gamma(x+alpha)*gamma(n-x+beta)}/
    {gamma(alpha)*gamma(beta)*gamma(alpha+beta+n)}
}
for (i in 1:m) {
  y.tmp[1] <- rbeta(1, 1, 1)
  x.tmp[1] <- rbinom(1, n, y.tmp[1])
  for (j in 2:(k+1)) {
    y.tmp[j] <- rbeta(1, x.tmp[j-1]+alpha, n-x.tmp[j-1]+beta)
    x.tmp[j] <- rbinom(1, n, y.tmp[j])}
  y[i] <- y.tmp[k+1]
  x[i] <- x.tmp[k+1]}
for (i in 1:(n+1)) {
  Gibbs[i] <- mean(dbinom(i-1, n, y))
  Exact[i] <- betabinom(i-1)} # 달라지는 부분. 

dataset <- rbind(Gibbs, Exact)
barplot(dataset, beside=TRUE, col=c("black", "white"),
        legend = rownames(dataset), ylim=c(0, 0.12))
title(main="Comparison of Two Probability Histograms", font.main=3)
axis(1, at=seq(2, 50, by=3), labels=c(1:17))

xmean1 <- mean(x)
xmean1

xmean2 <- mean(n*y)
xmean2