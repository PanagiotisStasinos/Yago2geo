Classification problem using vectors from neural embeddings on YAGO2geo locations

**Abstract.**
based on the neural algorithm  


SUBJECT AREA: Neural Embeddings
KEYWORDS: YAGO2geo, DeepWalk, Neural Embeddings, Classification

**1 INTRODUCTION**
using RDFs from YAGO2geo for United Kingdom territory  
OPTIMIZATION, choose best parameters, best distance type,
get best accuracy with the smallest vector length, use only most important features,
better and faster training   

**Motivations.**

**2 Constructing Weighted Yago2geo Graph**
read RDFs to get features of each location  
features :
 * OS_ID (unique ID for each location)  
 * OS_Name (name of location)   
 * OS_type (category type, 15 different categories)  
 * OS_Geometry (Polygon that represents location's boarders)  
    * OS_area (estimated from polygon)
    * OS_center (center of polygon)


**3 CLASSIFICATION**


**4 CONCLUSION (center distance)**
**PARAMETERS**  

*OS_TYPE CATEGORIES :*  
* include all locations from, therefore include all OS_type categories (15 categories)  
* don't include ...............   

*DISTANCE TYPE :* 
* center_distance
* polygon_distance

*WINDOW SIZE :* 


*NUMBER_OF_WALKS and NUMBER_OF_STEPS :* 

*FEATURE OF VECTORS :* 
* os_area


**CASES**  
*window sizes tested* [11, 21, 31, 41, 51, 61, 71, 81]
*number of walks and steps* 
*feature combinations* 

**4 CONCLUSION (polygon distance)**
