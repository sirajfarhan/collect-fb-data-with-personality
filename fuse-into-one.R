library(jsonlite)
library(dplyr)

files <- list.files("./dataset", pattern="*.json", full.names=TRUE)

data <- do.call(rbind, lapply(files, function(x) { fromJSON(x) }))

outliers <- data %>%
  group_by(url, personality) %>%
  summarize(count = n()) %>%
  group_by(url) %>%
  summarize(count = n()) %>%
  filter(count > 1)

data <- data %>% filter(!(url %in% outliers$url))
data <- data[!duplicated(data$url),]
write.csv(data, './dataset/profiles.csv')

data %>%
  group_by(personality) %>%
  summarize(count = n()) %>%
  arrange(count) %>%
  write.csv('./dataset/counts.csv')

jpeg('./dataset/dist.jpg', width=1200, height=800)
plot(as.factor(data$personality))
dev.off()
