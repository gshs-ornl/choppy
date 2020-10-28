        __  __ __   ___   ____  ____  __ __     
       /  ]|  |  | /   \ |    \|    \|  |  |    
      /  / |  |  ||     ||  o  )  o  )  |  |    
     /  /  |  _  ||  O  ||   _/|   _/|  ~  |    
    /   \_ |  |  ||     ||  |  |  |  |___, |    
    \     ||  |  ||     ||  |  |  |  |     |    
     \____||__|__| \___/ |__|  |__|  |____/     
                                       ((///&                     
                                     ((((& //////                 
                                    (((      ////////#            
                                   ((((      #//////////**        
                           @@@@@@@&(((//    ////////%    (*****   
                         @@,        @@//////////%@/          ****,
                        @             (@///////@               *, 
                       @                @////#@                @  
                      @                 %@///@                 ,@ 
                      @         %@@      @///@         ,@@      @ 
                      @        ,@@@@    @&///@         @@@@    &  
                       @         .     (@/////@         .      @  
                        @%            @%///////@@            @    
                            %      @@(//////////*@@@      @@@     
                          (((//////////////////**********,        
                         (((//////////////////**********,         
                        ((((/////////////////**********,&         
                       (#########(((((((((((((((((((((/*          
                      ((@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
                      %((@%@" ///////////////**********,.%%      
                     (((@%@" ///////////////**********, %%
                    (((/@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
                   (((//////////////////**********,              
                  ((((/////////////////**********,              
                #(//*&///////////////**********,/                
                (//**,,.   &/////////**********,.                 
               (//**,,,%        ////**********,.                  
              ((/***,,.             *********,                  
             #(/***,,.                  %***,                   
            #(//**,,.                                           
           &(//**,,.                                            
           (//**,,,#                   _______________          
          ((/***,,,                    ___  /__(_)_  /_____     
         #(//**,,.                     __  /__  /_  __/  _ \    
        #(//**,,.                      _  / _  / / /_ /  __/    
       %(//**,,.                       /_/  /_/  \__/ \___/     
       (//**,,.#                               
      ((/***,,*                v 0.1.0
     (/***,,."

# Instructions

## `choppy-lite` standalone file usage

	 usage: choppy-lite.py [-h] [-s SHAPE_ARCHIVE] [-r RASTER] [-x STATS]
	                       [-o OUTPUT_DIR] [-f OUTPUT_FORMAT] [-d OUTPUT_FILE] [-a]

	 Add values via command line to send to choppy

	 optional arguments:
		 -h, --help            show this help message and exit
		 -s SHAPE_ARCHIVE, --shape_archive SHAPE_ARCHIVE
		          The archived files to use to extract features and compare against the raster
		 -r RASTER, --raster RASTER
				  The rasterfile to use for retrieving zonals tats from
		 -x STATS, --stats STATS
				  Which stats should be used to to compute the zonal statistics
		 -o OUTPUT_DIR, --output-dir OUTPUT_DIR
				  Where should the file be stored	
		 -f OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
				  the type of format to output the file as
		 -d OUTPUT_FILE, --destination OUTPUT_FILE
				  the destination output file
		 -g, --geometry
		      export the geometry field
		 -a, --all-touched
				  should all touched shapes be included

Standard usage of the the choppy command line is `./choppy-lite.py -s <shapefile.zip> -r <raster.tif> -f xlsx -a` to create an Excel file of the zonal statistics using the all touched method and the default statistics of min, max, mean, median, majority, sum, std, and count. 

## Using included examples

Included in the `examples/` directory is a raster image of Nebraska produced via LandScan and a shape archive of county boundaries for Nebraska. Running the example is easy: `./choppy-lite.py -s examples/nebraska.zip -r examples/Neb_Landscan -f none -x "min,max,mean,std" -a -g` to produce `pandas` output.
