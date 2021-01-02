# Analyzing Top Brands in SafeGraph Neighborhood Patterns Data

SafeGraph provides timely information about the brands visitors to a neighborhood also visited during the same time period.  The data is provided in json through two columns in the Neighborhood Patterns schema: `top_same_month_brand` and `top_same_day_brand`.

> **Note:** The Neighborhood Patterns [schema](https://docs.safegraph.com/docs/neighborhood-patterns-2020) was [announced](https://www.safegraph.com/blog/announcing-neighborhood-patterns-safegraphs-newest-dataset) on July 7, 2020.  See [A Starter Guide for SafeGraph's Neighborhood Patterns and Real Estate Site Selection](https://colab.research.google.com/drive/1xiH77_MXdPcgPE8JqUYDfi9GqlhlHpJy?usp=sharing) for a helpful Jupyter-based introduction that includes instructions for obtaining the free [sample](https://www.safegraph.com/neighborhood-patterns) analyzed below. 

 ## **What is SafeGraph Neighborhood Patterns Data and what are "Top Brands"?**

SafeGraph Neighborhoods are census block groups (CBG)--areas the U.S. Census Bureau draws to contain 800 - 1,200 households each.  Each CBG is identified by a 12-digit string that nests a 2-digit state, a 3-digit county, a 6-digit census tract, and a 1-digit block code.  The United States (including Puerto Rico and the island areas) is comprised of over 220,000 CBGs. 

Here is SafeGraph Top Brands data from the June 2020 Neighborhood Patterns release for census block group #530330075005, which from June 8 through July 1 was the site of an occupation protest and self-declared autonomous zone in the Capitol Hill neighborhood of Seattle, Washington.

    #npatterns_raw.shape   (220684, 35)  The entire 2020 June Neighborhood Patterns sample (shown here as a pandas dataframe) is available from SafeGraph for free! 
    [In] npatterns_raw[npatterns_raw['area']=='530330075005'][['top_same_month_brand', 'top_same_day_brand']].values[0]
    [Out] array(['{"Starbucks":42,"Safeway":27,"Shell Oil":24,"McDonald\'s":23,"Chevron":22,"Walmart":19,"Target":19,"76":19,"Costco Wholesale Corp.":18,"7-Eleven":15,"Subway":15,"Safeway Pharmacy":14,"The Home Depot":13,"ARCO":13,"Safeway Fuel Station":12,"Taco Bell":12,"Jack in the Box":12,"QFC (Quality Food Centers)":12,"Fred Meyer":11,"Walgreens":11}', '{"Starbucks":6,"Shell Oil":3,"Poke Bar":2,"Blick Art Materials":2,"Safeway":2,"GTS Interior Supply":2,"GameStop":2,"Hyatt House":2,"76":2,"Emerald City Smoothie":2,"McDonald\'s":2,"Petco":1,"IHOP":1,"Toyota":1,"Menchie\'s":1,"Sonic":1,"Hallmark Cards":1,"Walmart":1,"Bahama Breeze":1,"Value Village Thrift Stores":1}'], dtype=object)

According to Neighborhood Patterns, 42% of the visitors to the Capitol Hill Organized Protest (CHOP) in June 2020 also visited Starbucks that month (c/o  `top_same_month_brand`).  

On the median day in June 2020, 6% of the day's visitors to the CHOP also visited Starbucks that day (c/o `top_same_day_brand`).

In comparison with an analogue to `top_same_month_brand` in the October 2018 Neighborhood Patterns release--also a free drop but one that provided only an unordered list of the top 10 same_month brands--visitors to CBG 530330075005 prior to CHOP preferred regional/small-box brands (7-Eleven, Bartell Drugs, ARCO) over national/big-box brands (McDonald's, Walmart, Target).

    [In] npatterns_raw_2018.rename(columns={'census_block_group': 'area', 'related_same_month_brand': 'top_same_month_brand'}, inplace=True)
    [In] npatterns_raw_2018[npatterns_raw_2018['area']=='530330075005']['top_same_month_brand'].values[0]
    [Out] '["starbucks","Safeway","Costco Wholesale Corp.","76","Shell Oil","Chevron","SUBWAY","7-Eleven US","Bartell Drugs","ARCO"]'

In general, `top_same_day_brand` has a much smaller range than `top_same_month_brand` and is skewed towards local/regional brands.  It's the better column when you want to study the brands visited by a customer on a typical day rather than the brands most customers visited anytime during a month.

## **Why analyze Top Brands data?**
It's useful!  A business owner can use it to identify opportunities for cross-promotion and co-branding.  Policymakers may find it useful for understanding the evolving preferences and habits of their citizenry.  Social science researchers will value its wide coverage and high frequency, which add power to any explanation of human behavior associated with specific times and places.

## **What's in this repository?**
This repository contains a [function]() that transforms SafeGraph Top Brands data into a matrix of Tf-Idf statistics.  Element <img src="https://render.githubusercontent.com/render/math?math=(i,j)"> in the matrix corresponds to the Tf-Idf of brand <img src="https://render.githubusercontent.com/render/math?math=j"> in geography <img src="https://render.githubusercontent.com/render/math?math=i">.  By analogy to Natural Language Processing, each brand is modeled as a "word" in a "corpus" of geographically-based "documents".
 
 ## **What is Tf-Idf and why calculate it?**
I love travel books.  Bear with me for a moment :slightly_smiling_face: 

Good travel books--Alexis de Tocqueville’s <em>Democracy in America</em>, Marquis de Custine’s <em>Letters from Russia</em>--tell us something interesting about every place they describe.  For instance, Marco Polo, in describing the district of Kamul glosses over its run-of-the-mill geography and religious practices but describes at length the custom of its men who, when visited at home by strangers “give positive orders to their wives, daughters, sisters, and other female relations, to indulge their guests in every wish, whilst they themselves leave their homes, and retire into the city, and the stranger lives in the house with the females as if they were his own wives”.  

 Information of questionable value, yet clearly “interesting”.

The formula for “interesting” in a good travel book is intuitive: write about something prevalent in a place but found nowhere else. It reminds me of a metric commonly used in Natural Language Processing called **term frequency-inverse document frequency (Tf-Idf)**.  

Tf-Idf is a metric for the importance of a word in a document. It is calculated as the product of two measures: (1) **term frequency**, which is the number of times a word is found in a document, and (2) **inverse document frequency**, which is the ratio of the number of unique documents in a corpus to the number of those documents that contain the word.  Thus the Tf-Idf scales the "raw" term frequency of a word by its rarity in the corpus.  A word in every document like <em>the</em> isn't scaled, but a word in few documents like <em>Kamul</em> is scaled up.

>This repository contains a [function]() that transforms SafeGraph Top Brands data into a matrix of Tf-Idf statistics.**  

Element <img src="https://render.githubusercontent.com/render/math?math=(i,j)"> in the resulting Tf-Idf matrix corresponds to the importance of brand <img src="https://render.githubusercontent.com/render/math?math=j"> in geography <img src="https://render.githubusercontent.com/render/math?math=i">, where each brand is modeled as a "word" in a "corpus" of geographically-based "documents".  

Just as a word is important in a document because it's used frequently in that document but not in all other documents, a brand is important because it's co-visited in that geography but not in all other related geographies.  

Thus, (1) viewing a "corpus" as a cohort consisting of all the geographies in a nation, state, or county, (2) viewing each geography (i.e. census block group) in this cohort as a "document", and (3) viewing co-visited brands as "words" in that document (their term frequency indicated by the percentages in  `top_same_month_brand` or `top_same_day_brand`), the theory behind Tf-Idf enables element <img src="https://render.githubusercontent.com/render/math?math=(i,j)"> of the matrix to be understood as brand <img src="https://render.githubusercontent.com/render/math?math=j">'s <em>importance</em> in census block group <img src="https://render.githubusercontent.com/render/math?math=i">, with respect to a relevant cohort.

 ## **Is there anything to be gained by looking at the world in this way?**
Yes.  

Tf-Idf metrics will differ most from the raw percentages in `top_same_month_brand` or `top_same_day_brand` when brands are rare.  

However, rarity is a relative term: brands can be popular in one part of the country yet completely unknown in another-- simultaneously. 

Tf-Idf recognizes this explicitly and forces the modeler to declare up-front the area over which "rarity" should be assessed.

What is gained?  Comparability, across space, time, and brands. 
 ## **So, how does the function work?**
>The primary [function]() is `brand_transformer`, which transforms SafeGraph Top Brands data into a <img src="https://render.githubusercontent.com/render/math?math=G \times B"> matrix of Tf-Idf statistics ('tfidf') and two companion dictionaries: one that indexes the matrix's <img src="https://render.githubusercontent.com/render/math?math=G"> geographies ('gidxs') and the other that indexes its <img src="https://render.githubusercontent.com/render/math?math=B"> brands ('bidxs').  This matrix contains all the information necessary for any kind of subsequent analysis of SafeGraph Top Brands data.

To illustrate its use, we begin by calling  `brand_transformer` to create two transformed objects based on `top_same_month_brand` for the analysis to follow: one for the contiguous United States (<em>usmonth</em>) and the other for King County, Washington (<em>kingmonth</em>).

    #brand_transformer(sgdf, period, cohort)
    #		sgdf = a Neighborhood Patterns release (dataframe)
    #		period = {'day', 'month'}
    #		cohort = {2-digit state, 5-digit county, 'us'}
    %%time
    [In] usmonth = brand_transformer(npatterns_raw, 'month', 'us')    
    [In] kingmonth = brand_transformer(npatterns_raw, 'month', '53033')
    [Out] CPU times: user 38.3 s, sys: 131 ms, total: 38.4 s
    Wall time: 38.5 s

A `brand_transformer` object includes a scipy.sparse matrix that either can be sliced horizontally to provide a <img src="https://render.githubusercontent.com/render/math?math=1 \times B"> importance vector describing a single CBG in "brand space," or vertically to provide a <img src="https://render.githubusercontent.com/render/math?math=G \times 1"> importance vector describing a single brand in physical space.

Here, a <img src="https://render.githubusercontent.com/render/math?math=1 \times B"> slice is used to learn more about CHOP in brand space.  We observe that there were 179 brands co-visited by visitors to King County.  Since SafeGraph currently only publishes the top 20 brands in any particular CBG, the view of any CBG in brand space will have only 20 non-zero entries.
 
    [In] km = kingmonth['tfidf'] #a scipy.sparse matrix in the brand_transformer object
    [In] km[kingmonth['gidxs']['530330075005'], :]
    [Out] <1x179 sparse matrix of type '<class 'numpy.float64'>'
	with 20 stored elements in Compressed Sparse Row format>

Suitable distance measures can be applied to quantify differences between CBGs in brand space.  We observe that among the visitors to the eight CBGs adjacent to CHOP,  those visiting the home CBG of the temporarily abandoned Seattle Police Department - East Precinct differed most from CHOP visitors in their list of important brands.  Turns out the other seven adjacent CBGS were anywhere from 25 to 49% closer to CHOP in brand space.  

    [In] chop = km[kingmonth['gidxs']['530330075005'], :].todense()
    [In] police = km[kingmonth['gidxs']['530330075004'], :].todense()
    [In] otheradj = km[kingmonth['gidxs']['530330074021'], :].todense()
    [In] scipy.spatial.distance.euclidean(chop, police)
    [Out] 90.93955453470048
    [In] scipy.spatial.distance.euclidean(chop, otheradj)
    [Out] 46.055058176046664

I wrote a function called `display_cbg`for a reader-friendly view of a CBG in brand space.  Nothing special (you can write your own): just a way of looking at the <img src="https://render.githubusercontent.com/render/math?math=1 \times B"> slice for CHOP as a dataframe.  
     
    [In] display_cbg('530330075005', kingmonth)
    [Out] 						530330075005
    Starbucks					42.000000
    Safeway						27.000000
    Walgreens					26.057662
    Safeway Pharmacy			24.948181
    Taco Bell					24.526998
    Shell Oil					24.000000
    McDonald's					23.000000
    Chevron						22.000000
    Target						19.323183
    Fred Meyer					19.302124
    QFC (Quality Food Centers)	19.276441
    Walmart						19.093695
    76						19.013357
    7-Eleven					18.753161
    Costco Wholesale Corp.		18.000000
    Jack in the Box				16.451175
    ARCO						15.667727
    Subway						15.525617
    The Home Depot				13.249032
    Safeway Fuel Station		13.224103
        
Set differences between the indices of the CHOP and police `display_cbg` outputs reveal that visitors to CHOP preferred Taco Bell over Poke for the munchies and emphasized shelter-in-place (Fred Meyer) over on-the-go (Costco Gasoline), when compared with visitors to the former home CBG of Seattle Police Department - East Precinct.   

    [In] set(display_cbg('530330075005', kingmonth).index).difference(set(display_cbg('530330075004', kingmonth).index))
    [Out] {'Fred Meyer', 'Taco Bell'}
    [In] set(display_cbg('530330075004', kingmonth).index).difference(set(display_cbg('530330075005', kingmonth).index))
    [Out] {'Costco Gasoline', 'Poke Bar'} 

Now, we take a <img src="https://render.githubusercontent.com/render/math?math=G \times 1"> slice of the  `brand_transformer` matrix object to learn more about Starbucks geographically.

In 142,072 of the 216,291 national CBGs, visitors also had visited a Starbucks that month. Think about that: at this very moment, there may be over 70,000 places in America with visitors who've gone a whole month without Starbucks!  :smirk:  

    [In] um = usmonth['tfidf'] #a scipy.sparse matrix in the brand_transformer object
    [In] um[:, usmonth['bidxs']['Starbucks']]
    [Out] <216291x1 sparse matrix of type '<class 'numpy.float64'>'
	with 142072 stored elements in Compressed Sparse Row format>

I wrote a function called `plot_brand_importance` to make a map of this slice.  Again, nothing special (you can write your own).

    [In] plot_brand_importance('Starbucks', usmonth)

Starbucks Brand Importance (national cohort)
![](https://i.ibb.co/8gbF42z/foo-3.png)
Starbucks's surprising rarity at a national level adds importance to the visits it receives from visitors to the CHOP.  This becomes evident through the up-scaling that occurs in CHOP's Tf-Idf statistics calculated on the national cohort, shown visually above and quantitatively below.
    [In] um[usmonth['gidxs']['530330075005'], usmonth['bidxs']['Starbucks']]
    [Out] 59.65211013698326

However, from a <img src="https://render.githubusercontent.com/render/math?math=G \times 1"> slice of the <em>kingmonth</em> `brand_transformer` object, we learn that Starbucks is ubiquitous in King County.    

    [In] km[:, kingmonth['bidxs']['Starbucks']]
        [Out] <1422x1 sparse matrix of type '<class 'numpy.float64'>'
    	with 1422 stored elements in Compressed Sparse Row format>

Thus, for Starbucks, Tf-Idf<img src="https://render.githubusercontent.com/render/math?math=\approx">Tf, a fact already confirmed above through comparison of the raw `top_same_month_brand` data with the transformed brand-slice based on the King County cohort.

So, a final comparision of CHOP with the rest of King County confirms what some already suspected: the revolution will not be televised ... nor sipped .
    [In] km_slice = km[:, kingmonth['bidxs']['Starbucks']]  
    [In] km[kingmonth['gidxs']['530330075005'], kingmonth['bidxs']['Starbucks']] > np.quantile(km_slice.todense(), .8)
    [Out] False
  

## **Why are there only 20 brands in the `top_same_month_brand` and `top_same_day_brand` columns?**

Sound logic on SafeGraph's part, I imagine.  

The June 2020 Neighborhood Patterns release, at 5.6GB, is already unwieldy.  Expanding the number of Top Brands beyond 20 would make it even larger.   

However, the preceding analysis shows potential pitfalls in an arbitrary cutoff.  Depending on the cohort most meaningful for a given application, some brands currently above the cutoff may belong below it and other brands below the cutoff may belong above it.  There is no way to know for sure until the relevant cohort is selected and the corresponding Tf-Idf statistics are calculated.

Fortunately, the Tf-Idf machinery in Python's sklearn module is lightning fast.  Moreover, with `top_same_month_brand` and `top_same_day_brand` provided for all brands, current truncation-induced upward bias in the Tf-Idf statistics will disappear. 

Perhaps a set of Tf-Idf matrices for national and state cohorts could be a separate product accompanying each monthly release of Neighborhood Patterns? 

Or maybe I should just be thankful CHOP was cleared before it became Kamul.

> Written with [StackEdit](https://stackedit.io/).