# Processing the labels of the raw data (6.8 in "Deep Learning with R")

group1_dir <- "/Users/sofia/comp150_project1/data/data1"
train_dir <- file.path(group1_dir, "train")

labels <- c()
texts <- c()

for (label_type in c("male", "female")) {
  label <- switch(label_type, male = 0, female = 1)
  dir_name <- file.path(train_dir, label_type)
  for (fname in list.files(dir_name, pattern = glob2rx("*.txt"), 
                           full.names = TRUE)) {
    texts <- c(texts, readChar(fname, file.info(fname)$size))
    labels <- c(labels, label)
  }
}

# All the docs are in texts and the female/male characterization in labels
is.vector(texts)
length(texts)

is.vector(labels)
length(labels)
is.vector(label)

head(labels)
str(texts) # structure
texts[1:2]
labels[1:2]

# Plots with tm package. (The lesser plots.)
install.packages("tm")  # for text mining
install.packages("SnowballC") # for text stemming
install.packages("wordcloud") # word-cloud generator 
install.packages("RColorBrewer") # color palettes
install.packages("ggplot2")
# Load
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")
library("ggplot2")

#Take just the 3 docs and Create a corpus in tm package
#texts_sub<-texts[1:3]
#labels_sub<-labels[1:3]
docs1<-VCorpus(VectorSource(texts))
names(docs1)

inspect(docs1[[1]])
docs2 <- tm_map(docs1, content_transformer(tolower))
# Remove numbers
docs3 <- tm_map(docs2, removeNumbers)
# Remove your own stop words
# specify your stopwords as a character vector
#docs2 <- tm_map(docs2, removeWords, c("blabla1", "blabla2")) 
# Remove punctuations
docs4 <- tm_map(docs3, removePunctuation)
# Eliminate extra white spaces
docs5 <- tm_map(docs4, stripWhitespace)

#The Doc Term frequency matrix 
dtm <- DocumentTermMatrix(docs5)

dimnames(dtm)
inspect(dtm)
findFreqTerms(dtm, 4)

m <- as.matrix(dtm) 
dim(m)    # Note that the number of words dropped from 227 to 207
#The number of words in each doc
rowSums(m)
#the max length of the docs_sub
max(rowSums(m))

freq <- sort(colSums(as.matrix(dtm)), decreasing=TRUE)
names(freq)
wof <- data.frame(word=names(freq), freq=freq)
head(freq)
wordcloud(words = wof$word, freq = wof$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

barplot(wof[1:20,]$freq, las = 2, names.arg = wof[1:20,]$word,
        col ="lightblue", main ="Most frequent words",
        ylab = "Word frequencies")


#########################
# The nice plots!
install.packages("quanteda")
library("quanteda")

Qda_corpus<-corpus(texts)
summary(Qda_corpus)
docvars(Qda_corpus, "Review")<-labels
summary(Qda_corpus)
tokenInfo <- summary(Qda_corpus)
tokenInfo[which.max(tokenInfo$Tokens), ] 

Qda_dfm <- Qda_corpus %>% 
  dfm( remove_punct = TRUE) %>%
  dfm_trim(min_termfreq = 10, verbose = FALSE)

set.seed(100)
textplot_wordcloud(Qda_dfm)

Qda_dfm %>%
  dfm(groups = "Review",  remove_punct = TRUE) %>%
  dfm_trim(min_termfreq = 10, verbose = FALSE) %>%
  textplot_wordcloud(comparison = TRUE)

Qda_dfm %>%
  dfm(groups = "Review",  remove_punct = TRUE) %>%
  dfm_trim(min_termfreq = 10, verbose = FALSE) %>%
  textplot_wordcloud(comparison = TRUE, colors = c('red', 'blue'))


review_dfm <- dfm(Qda_corpus, groups = "Review", remove_punct = TRUE)

# Calculate keyness and determine male speeches as target group
# the output is a data.frame of computed statistics and associated p-values,
# where the features scored name each row, 
# and the number of occurrences for both the target and reference groups
# For measure = "chi2" this is the chi-squared value, signed female if the
# observed value in the target exceeds its expected value
result_keyness <- textstat_keyness(review_dfm, target = 1)
# Plot estimated word keyness
textplot_keyness(result_keyness) 

head(textstat_keyness(review_dfm, target = 1))
#head(textstat_keyness(review_dfm, target = 1, measure="pmi"))

# plot 20 most frequent words in female speech
female_dfm <- 
  corpus_subset(Qda_corpus, Review == 1) %>%
  dfm(remove_punct = TRUE)
female_freq <- textstat_frequency(female_dfm)
head(female_freq, 10)
library("ggplot2")
ggplot(female_freq[1:20, ], aes(x = reorder(feature, frequency), y = frequency)) +
  geom_point() + 
  coord_flip() +
  labs(x = "20 most frequent words in female speech", y = "Frequency")


# plot 20 most frequent words in male speech
male_dfm <- 
  corpus_subset(Qda_corpus, Review == 0) %>%
  dfm(remove_punct = TRUE)
male_freq <- textstat_frequency(male_dfm)
head(male_freq, 10)
library("ggplot2")
ggplot(male_freq[1:20, ], aes(x = reorder(feature, frequency), y = frequency)) +
  geom_point() + 
  coord_flip() +
  labs(x = "20 most frequent words in male speech", y = "Frequency")

# Finally, texstat_frequency allows to plot the most frequent words in terms
# of relative frequency by group.

dfm_weight_rev <- Qda_corpus%>%
  dfm( remove_punct = TRUE) %>%
  dfm_weight(scheme = "prop")


# Calculate relative frequency by group
freq_weight <- textstat_frequency(dfm_weight_rev, n = 20, groups = "Review")

ggplot(data = freq_weight, aes(x = nrow(freq_weight):1, y = frequency)) +
  geom_point() +
  facet_wrap(~ group, scales = "free") +
  coord_flip() +
  scale_x_continuous(breaks = nrow(freq_weight):1,
                     labels = freq_weight$feature) +
  labs(x = NULL, y = "Relative frequency")


