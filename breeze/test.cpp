#include <iostream>
#include <curl/curl.h>

int main() {
    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);

    // Create a CURL object
    CURL* curl = curl_easy_init();

    // Set the URL
    curl_easy_setopt(curl, CURLOPT_URL, "https://api.icicidirect.com/breezeapi/api/v1/customerdetails");

    // Set the request headers
    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    // Set the payload
    const char* payload = "{\n    \"SessionToken\": \"29823364\",\n    \"AppKey\": \"650G7Z51z645540%&15~b93v5*4M!574\"\n}";
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload);

    // Set the headers
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    // Perform the HTTP GET request
    CURLcode res = curl_easy_perform(curl);

    // Check for errors
    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    return 0;
}
