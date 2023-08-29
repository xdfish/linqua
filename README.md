# LINQUA
## SETUP STEPS

1. install java runtime
2. install ffmpeg
```bash
$ brew install ffmpeg         //MacOS
$ sudo apt install ffmpeg     //Linux
```
3. Use [run.sh](backend/run.sh) script to setup backend application
```bash
$ bash run.sh setup
```

4. Use [run.sh](backend/run.sh) script to run server (in dev mode)
```bash
// In backend folder
$ bash run.sh dev
```

5. start frontend - in dev mode
        
```bash
// In frontend folder
$ npm run serve
```
6. Wait for application startup (could take up to 5min)


## RUN.SH Hints
Use [run.sh](backend/run.sh) script to setup or start server in development or production mode
```bash
$ bash run.sh setup
$ bash run.sh dev
$ bash run.sh prod
```


## GENERAL INFORMATION
Join Postman-Team: [Click Here](https://app.getpostman.com/join-team?invite_code=3ab5a9159a2423c81cd34ea790022164)