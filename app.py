import coc
from flask import Flask, request, abort, render_template
from flask_restful import Resource, Api
from json import dumps
import asyncio

app = Flask(__name__,static_url_path='/public', static_folder='public')
api = Api(app)
coc_client = coc.login('meszaros.laszlo.1987@gmail.com', 'JT7iw9Cde')
clan_tag = "#28Y8QULUU"
loop = asyncio.get_event_loop()

@app.route("/")
def homepage():
    return render_template('index.html', clan_tag=clan_tag)

@app.route("/tag/<string:tag>")
def member(tag):
    return render_template('tag.html', tag=tag)
    
class Members(Resource):
    def get(self, tag):
        tag = "#" + tag
        player = loop.run_until_complete(coc_client.get_player(tag))
        print(player)
        return {"best_trophies": player.best_trophies, "best_versus_trophies": player.best_versus_trophies,
        "war_stars": player.war_stars, "town_hall": player.town_hall, "builder_hall": player.builder_hall, "name": player.name}

api.add_resource(Members, '/members/<string:tag>')

class ClanMembers(Resource):
    def get(self):
        members = loop.run_until_complete(coc_client.get_members(clan_tag))

        return [{'tag': player.tag, 'name': player.name} for player in members]

api.add_resource(ClanMembers, '/clan_members')

if __name__ == "__main__": 
    app.run()