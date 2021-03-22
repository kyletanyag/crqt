import http.client as hc

httpHost    = "http://127.0.0.1";
httpMethod  = "GET";
url         = "/api/browse/zyxel";
headers     = {"Accept: text/html"};

# Connect to a HTTP server
hcon = hc.HTTPConnection("localhost",5000);

# Request for a URL
hcon.request(httpMethod, url);

# # Get the HTTP response
response = hcon.getresponse();

# # Read the HTTP response
html = response.read().decode();

# # Print HTML
print(html);