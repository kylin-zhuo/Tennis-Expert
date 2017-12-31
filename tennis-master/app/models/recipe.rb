class Recipe
  
  include HTTParty

  hostport = ENV["FOOD2FORK_SERVER_AND_PORT"] || 'www.food2fork.com'
  key_value = ENV["FOOD2FORK_KEY"]
  base_uri "#{hostport}/api"
  default_params key: key_value, fields: "image_url, title, social_rank, source_url"
  format :json

  def self.for term
    get("/search", query: {q: term})["recipes"]
  end

end
