library(dplyr)
library(tidyr)

# source data from web (pre-downloaded), reformat date, sort by date
all_data <- read.csv("owid-covid-data.csv")
all_data$date <- as.Date(all_data$date)
all_data <- all_data[order(all_data$date, decreasing=TRUE),]


# get countries data, such as poverty, gpd, no of hospital beds, etc.
country_data <- all_data %>% distinct(all_data$location, .keep_all = TRUE)

# change parameters of ordering in order to generate desired plot
ordered_data <- country_data[order(country_data$life_expectancy, decreasing=FALSE),]


# plot corelation between two indicators
par(mfrow=c(1,1))
plot(1:nrow(ordered_data), ordered_data$total_deaths_per_million, xlab="Procent obywateli powyżej 70 r.ż. (rosnąco)", ylab="śmiertelność na mln obywateli")

grid()
# human-dev-index ~ total deaths per million
# human-dev-index ~ total cases per million


# only countries, no other categories
##### all_data <- all_data[!(all_data$continent == "" | is.na(all_data$continent)), ]


str(all_data) # read structure of data frame, get to know all the headers

# get some subjective-picked regions 
poland_data <- all_data[all_data$location == "Poland", ]
germany_data <- all_data[all_data$location == "Germany", ]
EU_data <- all_data[all_data$location == "Europe", ]
ASIA_data <- all_data[all_data$location == "Asia", ]
china_data <- all_data[all_data$location == "China", ]
usa_data  <- all_data[all_data$location == "United States", ]


# data of continents
Continents_data <- rbind(head(all_data[all_data$location == "Asia", ], n=1), head(all_data[all_data$location == "Europe", ], n=1))
Continents_data <- rbind(Continents_data, head(all_data[all_data$location == "North America", ], n=1))
Continents_data <- rbind(Continents_data, head(all_data[all_data$location == "South America", ], n=1))
Continents_data <- rbind(Continents_data, head(all_data[all_data$location == "Oceania", ], n=1))
Continents_data <- rbind(Continents_data, head(all_data[all_data$location == "Africa", ], n=1))

#get desired index from continents
Continents_index <-  c(mean(all_data[all_data$continent == "Asia", ]$aged_70_older,na.rm=TRUE),
                                  mean(all_data[all_data$continent == "Europe", ]$aged_70_older,na.rm=TRUE),
                                  mean(all_data[all_data$continent == "North America", ]$aged_70_older,na.rm=TRUE),
                                  mean(all_data[all_data$continent == "South America", ]$aged_70_older,na.rm=TRUE),
                                  mean(all_data[all_data$continent == "Oceania", ]$aged_70_older,na.rm=TRUE),
                                  mean(all_data[all_data$continent == "Africa", ]$aged_70_older,na.rm=TRUE))
Continents_data["aged_70_older"] <- Continents_index



# plot barplots showing continent statistics
par(mfrow=c(2,1))
barplot(Continents_data$total_deaths_per_million, names.arg = Continents_data$location, main="Śmiertelność w przeliczeniu na milion mieszkańców")
grid()
barplot(Continents_data$total_cases_per_million, names.arg = Continents_data$location, main="Ilość Zakażeń w przeliczeniu na milion mieszkańców")
grid()
Continents_data$aged_70_older



par(mfrow=c(1,1))
plot(poland_data$date,poland_data$stringency_index , type="l", xaxt="n", col="red", ylim=c(0,100), xlab="Data", ylab = "Wskaźnik reakcji rządu [1]") # basic plot
axis(1, poland_data$date, format(poland_data$date), cex.axis = 1)
lines(germany_data$date,germany_data$stringency_index, col="green") # basic plot
lines(EU_data$date,EU_data$stringency_index, col="blue") # basic plot
lines(ASIA_data$date,ASIA_data$stringency_index, col="pink") # basic plot
lines(china_data$date,china_data$stringency_index, col="turquoise") # basic plot
lines(usa_data$date,usa_data$stringency_index, col="black") # basic plot
grid()
legend("bottom", legend=c("Poland", "Germany", "EU", "Asia", "China", "United States"),
       col=c("red", "green", "blue", "pink", "turquoise", "black"),lty=1)


?legend



  
  
  
