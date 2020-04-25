
# OpenStreeMap Case Study
***
## Bohemia, New York 

- https://www.openstreetmap.org/relation/175697

I chose this map because I grew up in this area. I thought it would be interesting to see how much has changed since I lived there.   

# `Problems Encountered`

   #### ` - Over Abbreviated Street Names`

   #### ` - Inconsistent or Erroneous tags`


## `Over Abbreviated Street Names:`
<hr>
Using the Case Study material. I used the code to find and update the street names.

```python

        def update(name):
          m = street_type_re.search(name).group()
          # If the street is abbreviated 
         if m not in expected:
              name = name.replace(m,mapping[m])
          return name
```

 
 I had to ensure these changes would reflect in the CSV files:

    For the nodes_tags file:

```python
        if tag.attrib['k'] == 'addr:street':
                            #update street names
                            nodes['value'] = update(tag.attrib['v'])
 ```           

    For the ways_tags file:

```python
        if tag.attrib['k'] == 'addr:street':
                            #update street names
                            tagt['value'] = update(tag.attrib['v'])
```                  

 ## `Inconsistent or Erroneous tags:`
 <hr>
 
 While checking for errors in postal codes:
 Taken from the Sample Project
 https://gist.github.com/carlward/54ec1c91b62a5f911c42
 
 ```sql
        SELECT tags.value as zipcode, COUNT(*) as count 
        FROM (SELECT * FROM nodes_tags 
	    UNION ALL 
        SELECT * FROM ways_tags) tags
        WHERE tags.key='postcode'
        GROUP BY tags.value
        ORDER BY count DESC;
```

|Zipcode|Count|
|-------|-----|
|11741	|5237|
|11722	|4522
|11782	|4036
|11716	|3015
|11752	|2849
|11769	|2496
|11779	|2407
|11705	|1999
|11730	|1886
|11796	|840
|11749	|833
|11751	|609
|11742	|332
|11788	|118
|11739	|14
|11701	|1

There was a single postcode 11701. It was obivious a bad postal code, so I wanted to look further into the file. 
I found the node tag with the bad postal code to be:

```sql
        SELECT * FROM nodes_tags
        WHERE  id = '4904677800'
```
|id	       |key	      |value   |type|
|----------|:---------|:-------|:----|
|4904677800|postcode  |11701   |addr|
|4904677800|street    |Broadway|addr|
|4904677800|amenity   |pharmacy|regular|
|4904677800|name	  |CVS	   |regular|

Checking the longitude and latitude from the id of the tags.

|lon	|lat
|-------|--------|
|-73.1725917|40.7639954|

These tags did identify the CVS,but the postal code and the street were completely wrong.
The actual street was Amityville Street and the postal code was 11752.
This one issue may seem insignificant, but it bears the question "How many other issues?"

# `Data Overview`

<hr>

### File Sizes

    Bohemia.osm.....93.2 MB
    Bohemia.db......65.1 MB 
    nodes.csv.......33.7 MB
    nodes_tags.csv..97.4 KB
    ways............3.15 MB 
    ways_nodes......10.9 MB
    ways_tags.......6.53 MB`
    
### Number of Unique Users

```sql
        SELECT COUNT(distinct(uid))as unique_users
        FROM (SELECT uid FROM nodes UNION SELECT uid FROM ways);
```
                              
|Unique Users|
|------------|
|403|

### Top Contributers

```sql
SELECT a.user, COUNT(user)as cnt
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways)a
GROUP BY a.user
ORDER by cnt DESC
LIMIT 10;
```
|User	|Count
|-------|------|
|MySuffolkNY	|155431
|SuffolkNY	|150433
|Northfork	|55004
|RI-Improve	|27940
|JoelManagua	|22372
|Easky30	|17050
|woodpeck_fixbot	|8630
|42429	|3886
|Unggo99	|3098
|bot-mode	|1023

### Number of Nodes

```sql
SELECT count(*) from nodes;
```
`413645`

### Number of Ways

```sql
SELECT count(*) from ways;
```

`50752`

# `Additional Ideas`

<hr>

There may be a need to add a standard or guideline when using 'shop' as a tag. I found a large disparity in the amount of tags used in combination with 'shop'. Over half had less than three tags. Here is the query I used [shops.sql](https://github.com/jscho12/Openstreetmap/blob/master/shops.sql) 
Automated mapping was most likely used for most of these tags, so a more complete tag combination may be hard to do. This would require local and manual edits. 
It might be interesting to partner with schools as a Geography lesson. This would teach the students, and help Openstreet map with the additional data.

# `Conclusion`

<hr>

Obvious, this data is by no means complete. I found, in general, the data fairly clean, when looking for street addresses or postal codes. A good automated mapping program could easily correct these errors. I was suprised by the incompleteness of the data, granted there was a huge amount of data, but considering the size and population, One would have thought it would be larger.  
