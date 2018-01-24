# Vacation Recommendation Engine  
  
In this project, I created a recommendation engine for vacation spots and activities across the globe based on user interests using Tripadvisor reviews as a proxy for user experiences.  
  
Key steps outlined below:  
  
Step 1: Scrape reviews from TripAdvisor (See [scrapy_atl_tripadvisor.py](https://github.com/shireen121/vacation_recommender/blob/master/scrapy_atl_tripadvisor.py))  
Step 2: Dimensionality reduction utilizing LDA topic modeling with reviews (See main_workbook.ipynb for Steps 2-4)  
Step 3: Calculate similarities between activities based on topic distribution of reviews  
Step 4: Create Recommendation Engine  
Step 5: Build Flask App (To be provided - demo of app available in presentation slides)  
