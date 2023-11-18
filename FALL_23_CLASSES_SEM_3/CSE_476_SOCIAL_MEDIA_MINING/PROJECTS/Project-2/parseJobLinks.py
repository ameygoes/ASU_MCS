from selenium import webdriver

# Initialize the WebDriver (choose the appropriate browser driver)
# Make sure you have the corresponding WebDriver installed and in your PATH.
driver = webdriver.Chrome()  # You can use other drivers like Firefox, Edge, etc.

url = "https://www.linkedin.com/jobs/view/3739950278/?alternateChannel=search&refId=pqZJzJry2L0A2kfuis%2B2uA%3D%3D&trackingId=R79xSxjuRVn4OBBQIXFL2w%3D%3D"
# Navigate to the URL of the web page
driver.get(url)  # Replace with the URL of the web page you're working with

try:
    # Find the element by its id attribute
    job_details = driver.find_element_by_id("job-details")
    
    # Print the text content of the element
    print(job_details.text)
    
except Exception as e:
    print("Element with id 'job-details' not found.")
    print(e)

# Close the WebDriver
driver.quit()
