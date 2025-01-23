# Resy Booking  :clipboard:
A bot made for non technical users to book dinner reservations at your favorite restaurant. Please keep payment information on your resy account when attempting to book reservations that require a deposit.

## Table of Contents:  
- [Configuration Options](#configuration-options)
- [Instructions](#instructions)  

## Configuration Options
>**int**: not surrounded by quotations in the configs.toml file, example: ```2```  
>**str**: surrounded by quotations ONLY in the configs.toml file, ex: ```"string"```
- ### :key:api_key
  - This is the public API key for all users. This value should not change from ```"ResyAPI api_key=\"VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5\""``` in the configs.toml file.

- ### :family:party_size: int
  - This is the total number of guests you wish to book for.
 
- ### :watch:military_booking_time: str
  - This is the time you wish to book in 24H military time. This should be formatted as HH:MM:SS.
 
- ### :calendar:date: str
  - This is the date you wish to book your reservation on. This should be formatted as YYYY-MM-DD.
 
- ### :toilet:desired_seating: str
  - This is the seating location you wish to get. This defaults to ```Dining Room```, but you can enter any value seen under times on a restaurants landing page as shown below.
    
    ![image](https://github.com/user-attachments/assets/76525c3f-eceb-4d1a-b1f1-0603804d4563)

- ### :computer:venue_url: str
  - This is the URL of the resaurant you wish to book at. Go to resy, find the restaurant you want and click it. When you are on the landing page copy the URL from the address bar.
 
    ![image](https://github.com/user-attachments/assets/4d9be5dc-ab43-4e77-8fac-d966804946ef)

- ### :incoming_envelope:polling_intervals: int
  - This is the number of seconds between HTTP requests to the resy servers when searching for an open booking. Lower numbers such as .5 or 1 second should be used when you know times are dropping and you start the bot right before. It's not advised to run the bot all day with polling every second or faster.

## Instructions
> Please remember to NOT run this several times in small clusters, resy will freeze accounts for 24hrs if multiple logins in short succession are detected!
1. Download the current release .exe and configs.toml, which can be found in the compressed source code folders.
2. Right click the configs.toml file and select "Edit in Notepad" to change settings to fit your needs, or leave it as is to enter information manually each time the application is ran. This can be changed anytime by setting a value to ```false```.
3. Follow the on screen instructions, that's it.
