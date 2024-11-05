import os
import googlemaps
from datetime import timedelta
from datetime import datetime, date, time

class driveTime:
    def __init__(self, origin, destination, arrival_time):
        self.client = googlemaps.Client(key= os.getenv("MAPS_KEY"))
        self.origin = origin
        self.arrival_time = arrival_time
        self.destination = destination

    def get_drive_time_departure(self):
        """
        Calculates the drive time from origin to destination with real-time traffic
        """
        result = self.client.distance_matrix(
            self.origin,
            self.destination,
            mode="driving",
            departure_time="now"
        )
        duration_in_traffic = result["rows"][0]["elements"][0].get("duration_in_traffic", {}).get("text", "No traffic data available")
        return duration_in_traffic

    def get_drive_time_arrival(self):
        """
        Calculates the drive time from origin to destination based on a specified
        arrival time
        """

        total_seconds = int(self.arrival_time.total_seconds())
        hours = total_seconds // 3600 % 24  
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Create a time object from the timedelta
        arrival_time_as_time = time(hour=hours, minute=minutes, second=seconds)

        arrival_datetime = datetime.combine(date.today(), arrival_time_as_time)

        # Convert to Unix timestamp
        arrival_time_timestamp = int(arrival_datetime.timestamp())

        result = self.client.distance_matrix(
            self.origin,
            self.destination,
            mode="driving",
            arrival_time = arrival_time_timestamp
        )
        duration = result["rows"][0]["elements"][0]["duration"]["value"]
        return duration
    
    def get_message(self):
        """
        Generates a message indicating the time to leave to arrive at the destination on time.
        """
        # Get trip duration in seconds
        duration_seconds = self.get_drive_time_arrival()

        total_seconds = int(self.arrival_time.total_seconds())
        hours = total_seconds // 3600 % 24  
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Create a time object from the timedelta
        arrival_time_as_time = time(hour=hours, minute=minutes, second=seconds)

        arrival_datetime = datetime.combine(date.today(), arrival_time_as_time)
        
        departure_datetime = arrival_datetime - timedelta(seconds=duration_seconds)
        
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        
        duration_text = f"{minutes}min" if hours == 0 else f"{hours}h {minutes}min"
        
        # Format the message with the calculated departure time and formatted duration
        message = (f"You have to leave before {departure_datetime.strftime('%I:%M %p')} "
                f"to arrive at {self.destination} on time. The trip will take approximately {duration_text}.")
        return message
