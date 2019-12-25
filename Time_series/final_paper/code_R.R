sales_df = read.csv('C:/GitHub/HomeWork/Time_series/final_paper/sales_df_acc.csv')

biz_list = c('분식전문점','양식음식점','일식음식점','중식음식점','치킨전문점','커피·음료','패스트푸드점','한식음식점')

sector_list = c('골목상권','발달상권','관광특구','전통시장')

biz = biz_list[1] 
for( biz in biz_list) {
  index = sales_df$TRDAR_SE_CD_NM == sector_list[1] & sales_df$SVC_INDUTY_CD_NM == biz 
  x = sales_df$THSMON_SELNG_AMT[index]
  
  x <- ts(x,frequency = 4)
  x_cmp <- decompose(x)
  
  name = paste('C:/GitHub/HomeWork/Time_series/final_paper/그림/',biz,sep = '')
  name = paste(name,'.jpg',sep = '')
  jpeg(name)
  plot(x_cmp)
  dev.off()
    
  season_rank = rank(x_cmp$seasonal[1:4])
  season_sd = sd(x_cmp$seasonal[1:4])
  
  x_tmp  = x_cmp$trend[21:24]
  y_tmp = c(19,20,21,22)
  
  y_1_trend = lm(y_tmp~x_tmp)$coefficients[-1]
  
  x_tmp  = x_cmp$trend[13:24]
  y_tmp = c(11,12,13,14,15,16,17,18,19,20,21,22)
  
  y_3_trend = lm(y_tmp~x_tmp)$coefficients[-1]
  
  random_mean = sum((x_cmp$random[3:24])**2)
  random_sd = sd(x_cmp$random[3:24])
  
  df = NULL
  
  df$sr = season_rank 
  df$ssd = season_sd
  df$y1trend = y_1_trend 
  df$y3trend = y_3_trend
  df$randommean = random_mean
  df$randomsd =random_sd
  
  link = paste('C:/GitHub/HomeWork/Time_series/final_paper/ts_r/',biz,sep = '')
  link = paste(link,'.csv',sep = '')
  write.csv(df,link,row.names=FALSE)}
