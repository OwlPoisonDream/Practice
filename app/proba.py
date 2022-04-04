#для тестирование модулей
import yadisk


yToken = yadisk.YaDisk(token="AQAAAABetchDAAfIOoTtzk4Bd0cNm0VX3nt7gWs")#яндекс диск токен


if __name__ == '__main__':
    print(yToken.check_token())# проверка токина на вход
    #print(yToken.get_disk_info())
    #yToken.upload("что.txt", "/что.txt")
    print(yToken.get_upload_link("/proba"))