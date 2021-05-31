import constants as C
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


# define the bucket, org, token and url of the InfluxDB instance
bucket = C.influxdb_bucket
org = C.influxdb_org
token = C.influxdb_token
url = C.influxdb_url

# create a client instance
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# alias the query_api method of client to query_api
query_api = client.query_api()


class Query:

    # function to query the InfluxDB with the given parameters and return results
    def querier(self, days, field):

        # write the query
        query = f'from(bucket: "{bucket}")\
        |> range(start: -{days}d)\
        |> filter(fn: (r) => r._field == "{field}")'

        # send the query to InfluxDB and store the response in result
        result = client.query_api().query(org=org, query=query)

        # process the response and store the data we need in results and return it to the calling function
        results = []
        for table in result:
            for record in table.records:
                if type(record.get_value()) != str:
                    results.append(record.get_value())
        return results

    def computer(self, input, climate_variable):
        # begin the response text by checking the input
        # and set units accordingly
        units = ""
        if(climate_variable == "usvh"):
            response_text = "Radiation in µSv/hr\n\n"
            units = "µSv/hr"
        elif(climate_variable == "temp"):
            response_text = "Temperature in °C\n\n"
            units = "°C"
        else:
            response_text = "Humidity %\n\n"
            units = "%"

        # Add the current value
        response_text += f"1. Current value : {input[-1]} {units}\n\n"
        # Add the last 10 values
        response_text += "2. Last 10 values : \n\n"
        for i in range(1, 10):
            response_text += str(input[-1 * i]) + " " + units + "\n"
        # Add the maximum value
        response_text += f"\n3. Maximum value : {max(input)} {units}\n\n"
        # Add the minimum value
        response_text += f"4. Minimum value : {min(input)} {units}\n\n"
        # Add the average value
        response_text += f"5. Average value : {round(sum(input)/len(input), 2)} {units}\n\n"

        return response_text

    def preprocessor(self, input):
        if(input != "all"):
            return self.computer(self.querier(60, input), input)
        else:
            climate_variables = ["usvh", "temp", "humid"]
            response_text = ""
            for i in climate_variables:
                response_text += self.computer(self.querier(60, i), i)
                response_text += "\n\n\n"
            return response_text

    def alertMonitor(self):

        # run queries for temperature, humidity, radioactivity
        temp = self.querier(1, "temp")
        humid = self.querier(1, "humid")
        usvh = self.querier(1, "usvh")

        response_text = ""

        if(temp[-1] > 25):
            response_text += f"ALERT! TEMPERATURE THRESHOLD EXCEEDED! LAST TEMPERATURE VALUE = {temp[-1]} °C\n\n"
    
        if(humid[-1] > 25):
            response_text += f"ALERT! HUMIDITY THRESHOLD EXCEEDED! LAST HUMIDITY VALUE = {humid[-1]} %\n\n"

        if(usvh[-1] > 1.00):
            response_text += f"ALERT! RADIOACTIVITY THRESHOLD EXCEEDED! LAST RADIATION VALUE = {usvh[-1]} µSv/hr\\n\n"

        return response_text


