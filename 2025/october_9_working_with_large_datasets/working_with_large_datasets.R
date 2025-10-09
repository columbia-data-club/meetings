# find your current working directory  
getwd()

# set up your working directory
# my working directory in today's demo will be in a folder called Rdemo
setwd("C:/Users/wy2288/Downloads/Rdemo")

# install following packages if you cannot find them listed under the "Packages" tab in your RStudio
install.packages(c("tidyverse", "data.table", "arrow", "duckplyr"))

# use data.table; mostly for delimited separated files such as csv 
library(data.table)
system.time(
  basic_fread <- 
              fread(file ="basicincident.txt", 
                    sep = "^")
            )
# it takes 156 seconds on my laptop. 
# the size is 10.7 GB, which is much bigger than the txt file it self!
# And if our goal is to export the data later, maybe using parquet format is better.

gc() # garbage collection
rm(basic_fread) # if I don't remove basic_fread from my environment, there is not enough memory for creating basic_arrow file in the next step

#I would restart my R session and try the following code
# use arrow
library(arrow)
system.time(
  basic_arrow <- 
              read_delim_arrow(file ="basicincident.txt",
                               delim = "^")
            )
# it takes 28 seconds on my laptop
gc()

write_parquet(basic_arrow, sink = "basic.parquet")
# 985 MB parquet file saved in my folder

rm(basic_arrow)
# then restart R session

# Now let's use duckplyr instead of data.table & arrow
# because duckplyr is a DuckDB-backed drop-in replacement for dplyr, we can use any syntax we use in dplyr

library(duckplyr)
# since we have created the basic.parquet file, it might be a good idea to import basic.parquet directly
basic_duckdb <- 
  read_parquet_duckdb("basic.parquet") %>% 
  as_duckdb_tibble() 

nrow(basic_duckdb) # 33,312,139
head(basic_duckdb)
str(basic_duckdb)

# Alternatively, you can also use read_file_duckdb to import basicincidents.txt, which is the raw data file from OpenFEMA website
basic_duckdb2 <- 
  read_file_duckdb("basicincident.txt",
                   table_function = "read_csv_auto",
                   options = list(delim = "^",
                                  ignore_errors = TRUE)) %>% 
  as_duckdb_tibble()

nrow(basic_duckdb2) # 27,188,264
compute_parquet(basic_duckdb2, path = "basic2.parquet")

# Now we know we removed a lot of rows by setting the ignore_errors = TRUE. That's due to R's data type coercion rule. When data points in the same column are with more than 1 type, it must be converted into a single type. 
# Here is a chunk for converting all the columns into character type. For many columns, if there are any NA/NULL/no/U/UU/UUU values, the columns cannot be read and converted into tibble using read_file_duckdb() unless you convert those columns as char. 

library(duckplyr)

basic_duckdb_char <- 
  read_file_duckdb("basicincident.txt",
                   table_function = "read_csv_auto",
                   options = list(delim = "^",
                                  types = list(c("VARCHAR","VARCHAR","VARCHAR", "VARCHAR","VARCHAR", "VARCHAR", "VARCHAR","VARCHAR" ,"VARCHAR" ,"VARCHAR" ,"VARCHAR" , "VARCHAR", "VARCHAR","VARCHAR", "VARCHAR", "VARCHAR","VARCHAR" ,"VARCHAR" ,"VARCHAR" ,"VARCHAR" , "VARCHAR", "VARCHAR","VARCHAR", "VARCHAR", "VARCHAR","VARCHAR" ,"VARCHAR" ,"VARCHAR" ,"VARCHAR" , "VARCHAR", "VARCHAR","VARCHAR","VARCHAR", "VARCHAR","VARCHAR" ,"VARCHAR" ,"VARCHAR" ,"VARCHAR" , "VARCHAR", "VARCHAR","VARCHAR","VARCHAR")))) %>% 
  as_duckdb_tibble()

a <- basic_duckdb_char %>% filter(INCIDENT_KEY == "AK_23200_08292024_0012850_0")

library(stringr)
A <- basic_duckdb %>% filter(str_detect(INCIDENT_KEY, "^AK_23200"))

# read causes.txt using the same function
causes_duckdb <- 
  read_file_duckdb("causes.txt", 
                   table_function = "read_csv_auto",
                   options = list(delim = "^")
                   ) %>% 
  as_duckdb_tibble() %>% 
  mutate(across(c(INC_DATE:EXP_NO), as.integer))

compute_parquet(causes_duckdb, path = "causes.parquet")

# Now we can restart R sessions and use parquet files instead of txt files
# try inner join for the two parquet files
bsc_par <- read_parquet_duckdb("basic.parquet") %>% 
  as_duckdb_tibble() 

caus_par <- read_parquet_duckdb("causes.parquet") %>% 
  as_duckdb_tibble()
  
joined_accident <- bsc_par %>%
  inner_join(caus_par, 
             by = c("INCIDENT_KEY" = "INCIDENT_KEY", 
                    "STATE" = "STATE", 
                    "FDID" = "FDID",
                    "INC_DATE" = "INC_DATE",
                    "INC_NO" = "INC_NO",
                    "EXP_NO" = "EXP_NO")
             )

joined_accident[1:6, 42:45]
unique(joined_accident$STATE)
compute_parquet(joined_accident, path = "joined.parquet")

# use read_file_duckdb to read incident address file
incadd_duckdb <- 
  read_file_duckdb("incidentaddress.txt", 
                  table_function = "read_csv_auto",
                  options = list(delim = "^",
                                 ignore_errors = TRUE)) %>% 
  as_duckdb_tibble()

write_parquet(incadd_duckdb, sink = "incadd.parquet") # from package arrow

compute_parquet(incadd_duckdb, path = "incadd2.parquet") # from package duckplyr

# so far I have loaded multiple data files in RStudio and the memory usage seems still manageable. And it should be fine if you'd like to do more merges.

# restart R session

# The following chunk is using ggplot() for some visualizations; this is just show you once data is imported using as_duckdb_tibble(), you can use any tidyverse functions for data manipulation (such as ggplot2)

library(ggplot2) 
joined_accident <- read_parquet_duckdb("joined.parquet") %>% 
  as_duckdb_tibble() 

mansions <- 
  joined_accident %>% 
  filter(!is.na(PROP_VAL) , PROP_VAL > 1e7 ) 

mansions%>% 
  ggplot(aes(x = GCC, y= PROP_VAL)) + geom_boxplot()

death <- joined_accident %>% 
  filter(FF_DEATH >0)

injury <- joined_accident %>% 
  filter(FF_INJ >0)

injury %>% 
  ggplot(aes(x = GCC, y= FF_INJ)) + geom_boxplot()


# If we still have time today, we can look into how to use url link import data

# We will try to download the seattle-library-checkouts.csv, which is almost 9 GB
# Don't run the following code chunk until you are confident with current internet speed (it might take up to 10 min or even longer for downloading); the code & url link is from the online book "R for Data Science" 
curl::multi_download(
  "https://r4ds.s3.us-west-2.amazonaws.com/seattle-library-checkouts.csv",
  "seattle-library-checkouts.csv",
  resume = TRUE
)

# if I have downloaded it in my local folder, I can also import it using the following code chunk
checkouts <- 
  read_file_duckdb("seattle-library-checkouts.csv", table_function = "read_csv_auto") %>% 
  as_duckdb_tibble()

# Alternatively, there is a way using duckplyr

db_exec("INSTALL httpfs")
db_exec("LOAD httpfs")

url <- "https://r4ds.s3.us-west-2.amazonaws.com/seattle-library-checkouts.csv"
checkouts_csv <- read_csv_duckdb(url)

# glimpse(checkouts) # glimpse function from tidyverse package takes a long time and it won't show you the row numbers!

# The same as we have tried above, we can convert it as parquet using write_parquet() function from package arrow 
write_parquet(checkouts, 
              sink = "checkouts-arrow.parquet")
## it will take a while to finish. 
## 4.09 GB on my computer
## Maybe duckplyr is faster. Let's try.

# compute_parquet() function from package duckplyr, which can produce the parquet file faster
compute_parquet(checkouts, 
                path = "checkouts-duckdb.parquet")
# this parquet file is 4.13 GB on my computer

# You can try a different memory protection mode
compute_parquet(checkouts,
                path = "checkouts-duckdb-stingy.parquet",
                prudence = "stingy")
# it takes much longer than the default way above
# the same 4.13 GB on my computer


