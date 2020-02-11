package org.northcoder.dockerunirest;

import kong.unirest.HttpResponse;
import kong.unirest.Unirest;
import kong.unirest.JsonNode;
import kong.unirest.json.JSONArray;
import kong.unirest.json.JSONObject;

public class App {

    public static void main(String[] args) {
        App app = new App();
        app.listImages();
        app.startContainer();
    }

    private void listImages() {
        String url = "http://localhost:2375/images/json";
        JSONArray array = Unirest.get(url)
                .header("accept", "application/json")
                .asJson()
                .getBody()
                .getArray();

        for (int i = 0; i < array.length(); i++) {
            JSONObject image = array.getJSONObject(i);
            String s = image.getString("RepoTags");
            System.out.println(s);
        }
    }

    private void startContainer() {
        String url = "http://localhost:2375/containers/imdb_test/start";
        HttpResponse<JsonNode> response = Unirest.post(url)
                .header("accept", "application/json")
                .asJson();
        System.out.println(response.getStatus() + " - "
                + response.getStatusText());
    }

}
