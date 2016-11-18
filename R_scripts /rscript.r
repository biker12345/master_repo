	# Time series analysis for hotels 
	#
	# @author - saurabh ,dishari
  
	library('forecast')
	# function to initialize the train data from the csv data variable load_data  
	load_data =  read.table("/home/nagababu/Desktop/c.csv",header=TRUE,sep=",")

	date_list = function(start_month,end_month,no_of_days_list){
		x = 1
		date = list()  
		for(i in start_month:end_month){
			j=1
			year = '2016'
			while(j < no_of_days_list[i]){
				if (x > window_size){
					break;
				}
				if ( j < 10 ){
					if(i < 10){
						date_text = paste('0',toString(j),'-','0',toString(i),'-',year,sep="")
					}
					else {
						date_text = paste('0',toString(j),'-',toString(i),'-',year,sep="")
					}
				}
				else{
					if(i < 10){
						date_text = paste(toString(j),'-','0',toString(i),'-',year,sep="")
					}
					else {
						date_text = paste(toString(j),'-',toString(i),'-',year,sep="")
					}
				}
				j = j+1
				date[x] = date_text
				x = x+1
			}
		}
		#print(unlist(date))
		return (date)
	}

	initialize_data = function(train_data,date,load_data) {
		#load data from local file
		x = 1  
		for (i in 1:window_size){
			if(date[[i]] == paste(substring(load_data$days[x],7,8),substring(load_data$days[x],5,6),substring(load_data$days[x],1,4),sep="-")){
				train_data[i] = load_data$Txns[x]
				x = x+1	
			}
			else
				train_data[i] = 0
		}
		#print(unlist(train_data))
		return(train_data)
	}

	get_day_of_week = function(day,date_to_day_map,date){
		for (i in 1:window_size){
			day[i] = date_to_day_map[[ weekdays(as.Date(date[[i]],'%d-%m-%Y'))]]
		}
		#print(unlist(day))
		return(day)
	}

	calculate_moving_average = function(moving_average_list,train_data){
		#loop and get the values and calculate the moving average 
		for (i in 1:window_size){
		# calculation starts from 4 the element with window of seven elements to make an average
		# first three elements are zero and last three elements are zero  
			if (i <= 3 || i > 207 ){
				moving_average_list[i] = 0
				next
			}
			buffer = 0 ;
		# add the seven value window and calculate the average  
			for (j in 0:6) {
				x = i-3+j
				buffer = buffer + train_data[[x]];
			}
			moving_average_list[i] = (buffer/7);
		}
		#print(unlist(moving_average_list))
		return (moving_average_list)
		
	}


	#function to calculate the seasonality and irregualr components 
	calculate_seasonality_and_irregularity   = function(seasonal_and_irregular,moving_average_list,train_data){
		# initialize the list with zero
		for (i in 1:window_size){
			seasonal_and_irregular [i] = 0
		}
		# calculate the seasonal and irregualr component combination 
		for(i in 1:window_size){
			#calcualtion for only non zero values 
			if( moving_average_list[[i]] != 0)
				seasonal_and_irregular[i] = train_data[[i]]/moving_average_list[[i]]
		}
		#print(unlist(seasonal_and_irregular))
		return(seasonal_and_irregular)
	}  

	# extracting only the seasonal component values from the seasonal and irregular component combination list  
	calculate_seasonality_only = function(seasonal_only,seasonal_and_irregular){
		for (i in 1:7){
			zero_count = 30
			x = 0
			# count the number of zero elements 
			while (x < 204 ){
				if (seasonal_and_irregular[[i+x]] == 0){
					
					zero_count = zero_count - 1	
				}
				x = x+7 

			}
			# calculate the seasonal component and make list of seasonal_only
			x  = 0 
			for(s in 0:203){
				x = x + seasonal_and_irregular[[i+s]]
				s  = s + 7 	

			}
			sum_var = 0
			while(sum_var < 204){
				seasonal_only[i+sum_var] = x/zero_count
				#print(sum_var) 
				sum_var = sum_var + 7
				#print (sum_var+i)
			}
			
		}
		#print(unlist(seasonal_only))	
		return(seasonal_only)
	}



	# function to calculate denormalize data 
	denormalize_data = function(normalize ,train_data,seasonal_only){
		for (i in 1:window_size){
			normalize[i] = seasonal_only[[i]]/train_data[[i]]
		}
		
		return(normalize)
	}


	#forcast method to get the result 
	forcast_the_data = function(result_forcast,day,seasonal_only){
		# calculate the linear regression
		x =c(1:window_size)
		day_of_week = c(unlist(day))
		y = c(unlist(seasonal_only))
		linn = data.frame(x,y) 	
		linear_reg = lm(y~x)
		# calculate the result forcast 
		
		#print(summary(linear_reg))
		for (i in 1:window_size){
	 		result_forcast[i] = round (seasonal_only[[i]] * (linear_reg$coefficients[1][1]+(linear_reg$coefficients[2][1]*i)) )
			if (result_forcast[i] < 0){
				result_forcast[i] = 0
			}
		}

		return (result_forcast)
	} 

	no_of_days_list = list(32,29,32,31,32,31,32,32,31,32,31,32)
	window_size = 210
	date_to_day_map = list("Monday"=1,"Tuesday"=2,"Wednesday"=3,"Thursday"=4,"Friday"=5,"Saturday"=6,"Sunday"=7)
	day = list()
	train_data = list()
	#moving average empty list 
	moving_average_list = list()
	# seasonal and irregular component empty list 
	seasonal_and_irregular = list()
	# seasonal component empty list 
	seasonal_only = list()
	# denomarlize empty list 
	normalize = list()
	# forcast result empty list 
	result_forcast = list()
	date = list()
	date = date_list(3,9,no_of_days_list)
	train_data=initialize_data(train_data,date,load_data) 
	day = get_day_of_week(day,date_to_day_map,date)
	moving_average_list=calculate_moving_average(moving_average_list,train_data)
	seasonal_and_irregular=calculate_seasonality_and_irregularity(seasonal_and_irregular,moving_average_list,train_data)
	seasonal_only= calculate_seasonality_only(seasonal_only,seasonal_and_irregular)
	normalize= denormalize_data(normalize,train_data,seasonal_only)
	result_forcast= forcast_the_data(result_forcast,day,seasonal_only)
	
