# -*- coding: utf-8 -*-
import scrapy
import json
import re

class SofifaSpider(scrapy.Spider):
    name = 'players_stats'

    custom_settings = {
        'ITEM_PIPELINES': {
            'fifa_scrapy.pipelines.FifaScrapyPipeline_Stats': 300,
        }
    }

    def __init__(self):
        with open('../data/json/players_url.json') as json_data:
            self.players = json.load(json_data)
        self.player_count = 1
        self.errorList = []

    def start_requests(self):
        urls = [
            'https://sofifa.com/player/158023?units=mks'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        try:
            for player in response.css('.info'):

                # Player Info
                player_name = player.xpath('//div[@class="info"]/h1/text()').extract()[0]
                player_info = player.xpath(
                    '//div[@class="info"]/div[@class="meta bp3-text-overflow-ellipsis"]//text()').extract()
                player_url_photo = player.xpath('//div[@class="bp3-card player"]//img/@data-src').extract_first()
                player_info = [info for info in player_info if info != ' ']
                player_overall_rating = player.xpath('(//section[@class="spacing"])[1]//span//text()').extract_first()
                player_potential = player.xpath('(//section[@class="spacing"]//span)[2]/text()').extract()[0]
                player_value = player.xpath('(//section[@class="spacing"]/div/div[3]//text())[1]').re(r'[\d.]*\d+')[0]
                player_wages = player.xpath('(//section[@class="spacing"]/div/div[4]//text())[1]').re(r'[\d.]*\d+')[0]
                player_teams = player.xpath('//div[@class="player-card double-spacing"]/h5/a/text()').extract()
                player_best = player.xpath('(//div[@class="column col-4"])[1]//li/span/text()').extract()

                # Lionel Andrés Messi Cuccittini (ID: 158023)
                player_name = player_name[:-14]

                # ['32y.o.', '(Jun', '24,', '1987)', '170cm', '72kg']
                age, month, day, year, height, weight = player_info[-1].split()
                age = int(re.match('\d+', age).group(0))  # Only digits
                month = month.replace('(', '')
                day = int(day.replace(',', ''))
                year = int(year.replace(')', ''))
                height = int(height.replace('cm', ''))
                weight = int(weight.replace('kg', ''))

                # ['Juventus', 'Portugal']
                if len(player_teams) == 2:
                    football_club, national_team = player_teams
                else:
                    football_club = player_teams[0]
                    national_team = ""

                # ['ST', '93']
                best_position, best_rating = player_best

                player_overall_rating = int(player_overall_rating)
                player_potential = int(player_potential)
                player_value = float(player_value)
                player_wages = float(player_wages)
                best_rating = int(best_rating)

                # Player Profile
                player_profile_label = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[1]//label/text()').extract()
                player_preferred_foot = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[1]/text()').extract()[
                    0]
                player_weak_foot = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[2]/text()')[
                    0].extract().strip()
                player_skill_moves = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[3]/text()')[
                    0].extract().strip()
                player_reputation = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[4]/text()')[
                    0].extract().strip()
                player_work_rate = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[5]/span/text()').extract()[
                    0]
                player_body_type = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[6]/span/text()').extract()[
                    0]
                player_real_face = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[7]/span/text()').extract()[
                    0]
                player_release_clause = player.xpath(
                    '((//div[@class="bp3-card double-spacing"])[1]//li[@class="bp3-text-overflow-ellipsis"])[8]/span/text()').re(
                    r'[\d.]*\d+')

                player_weak_foot = int(player_weak_foot)
                player_skill_moves = int(player_skill_moves)
                player_reputation = int(player_reputation)

                if player_release_clause:
                    player_release_clause = player_release_clause[0]
                    player_release_clause = float(player_release_clause)

                profiles = {k: v for k, v in zip(player_profile_label,
                                                 [player_preferred_foot, player_weak_foot, player_skill_moves,
                                                  player_reputation, player_work_rate, player_body_type,
                                                  player_real_face, player_release_clause])}

                # Player Stats
                player_attacking_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[3]//span[@class="tooltip multiline"]/text()').extract()
                player_attacking_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[3]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_skill_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[4]//span[@class="tooltip multiline"]/text()').extract()
                player_skill_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[4]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_movement_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[5]//span[@class="tooltip multiline"]/text()').extract()
                player_movement_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[5]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_power_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[6]//span[@class="tooltip multiline"]/text()').extract()
                player_power_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[6]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_mentality_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[7]//span[@class="tooltip multiline"]/text()').extract()
                player_mentality_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[7]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_defending_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[8]//span[@class="tooltip multiline"]/text()').extract()
                player_defending_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[8]//span[contains(@class,"bp3-tag")]/text()').extract()
                player_goalkeeping_labels = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[9]//span[@class="tooltip multiline"]/text()').extract()
                player_goalkeeping_values = player.xpath(
                    '(//div[@class="bp3-card double-spacing"])[9]//span[contains(@class,"bp3-tag")]/text()').extract()

                attacking = {k.replace(' ', ''): int(v) for k, v in
                             zip(player_attacking_labels, player_attacking_values)}
                skill = {k.replace(' ', ''): int(v) for k, v in
                         zip(player_skill_labels, player_skill_values)}
                movement = {k.replace(' ', ''): int(v) for k, v in
                            zip(player_movement_labels, player_movement_values)}
                power = {k.replace(' ', ''): int(v) for k, v in
                         zip(player_power_labels, player_power_values)}
                mentality = {k.replace(' ', ''): int(v) for k, v in
                             zip(player_mentality_labels, player_mentality_values)}
                defending = {k.replace(' ', ''): int(v) for k, v in
                             zip(player_defending_labels, player_defending_values)}
                goalkeeping = {k.replace(' ', ''): int(v) for k, v in
                               zip(player_goalkeeping_labels, player_goalkeeping_values)}

                player_info_dict = {
                    'name': player_name,
                    'photo_url': player_url_photo,
                    'positions': ','.join([position for position in player_info if position.isupper()]),
                    'age': age,
                    'birth_date': '{}/{}/{}'.format(year, month, day),
                    'height': height,
                    'weight': weight,
                    'football_club': football_club,
                    'national_team': national_team,
                    'overall_rating': player_overall_rating,
                    'potential': player_potential,
                    'value': player_value,
                    'wages': player_wages,
                    'best_position': best_position,
                    'best_rating': best_rating,
                }
                player_info_dict.update(profiles)
                player_info_dict.update(attacking)
                player_info_dict.update(skill)
                player_info_dict.update(movement)
                player_info_dict.update(power)
                player_info_dict.update(mentality)
                player_info_dict.update(defending)
                player_info_dict.update(goalkeeping)

                yield player_info_dict

                if self.player_count < len(self.players):
                    next_page_url = 'https://sofifa.com' + self.players[self.player_count][
                        'player_url'] + '?units=mks'
                    print(next_page_url)
                    self.player_count += 1
                    yield scrapy.Request(url=next_page_url, callback=self.parse)

        except Exception as e:
            print('Error: ' + player_name)
            print(e)
            self.errorList.append(response.url)

            if self.player_count < len(self.players):
                next_page_url = 'https://sofifa.com' + self.players[self.player_count][
                    'player_url'] + '?units=mks'
                # print(next_page_url)
                self.player_count += 1
                yield scrapy.Request(url=next_page_url, callback=self.parse)

            return
        finally:
            print(self.errorList)
