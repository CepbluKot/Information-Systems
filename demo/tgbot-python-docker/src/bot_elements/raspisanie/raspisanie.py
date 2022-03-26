import asyncio, time, parsers.full_pars_2 as full_pars_2


async def rasp_notification(group):
    rasp = full_pars_2.parse_group_today(group)
    while True:

        #  rasp = full_pars_2.parse_group_today(group) - ЗАПИХНИ ЭТО В САМОЕ НАЯАЛО ПЕРЕД ВСЕМИ ФУНКЦИЯМИ

        await asyncio.sleep(1)
        for data in rasp:
            time_diff = -(int(time.localtime().tm_hour) * 60 + int(time.localtime().tm_min)) + \
                int(data['time_start_hour']) * 60 + \
                int(data['time_start_minutes'])
            if time_diff <= 15 and time_diff > 0:
                pass
                # for user in data['notify']:
                #     if int(user['notify_status']) != 1:
                #         await bot.send_message(user['user'], str(data['name']) + ' через {0} минут'.format(time_diff))
                #         user['notify_status'] = 1
            # print(time_diff, data['name'])
