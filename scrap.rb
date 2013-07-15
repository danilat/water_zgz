#!/usr/bin/env ruby -wKU
 
require 'open-uri'
require 'json'
require 'pp'
require 'hpricot'
 
response = open('http://www.zaragoza.es/georref/json/hilo/ver_IMSP').read
data = JSON.parse(response)
 
def scrap(link)
    resp = open(link).read.encode("UTF-8")
    plum = Hpricot(resp)
 
    # Ok, this should get us the div class="elementos"
    elements = (plum/"/html/body/div/div[2]/div[2]/div[3]/div/div")
    table = (elements/"/table")
 
    indicators = {}
    category = ""
    (table/"/tr").drop(1).each do |tr|
        unless (tr/"/td/strong").inner_html.empty?
            category = (tr/"/td/strong").inner_html.force_encoding('UTF-8')
            indicators[category] = {}
        else
            thing = tr/"/td"
            name = thing[0].inner_html.force_encoding('UTF-8')
            value = thing[1].inner_html.force_encoding('UTF-8')
            indicators[category][name] = value
        end
    end
    indicators
end
 
deposits = []
data['features'].each { |feature|
    deposit = {}
    link = feature['properties']['link']
 
    deposit['title'] = feature['properties']['title']
    deposit['description'] = feature['properties']['description']
    deposit['date'] = feature['properties']['date']
    deposit['UTM_position'] = feature['geometry']['coordinates']
    #deposit['latlon_position'] = TODO
    deposit['link'] = link
    deposit['indicators'] = scrap(link)
 
    deposits << deposit
}
 
PP.pp(deposits)