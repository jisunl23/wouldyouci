# REST API

# 백앤드 주소  [https://](http://15.164.96.65:80/)wouldyouci.ga

- 5/25 재배포 완료
- 5/26 재배포 완료

# 5/27 수요일 오늘의 ngrok [http://19977cf3.ngrok.io](http://19977cf3.ngrok.io/)

# Notice

- 질문 달아주시면 확인하는대로 답변 드립니다.
- `blah` 된 것은 만든 API, 안 된 것은 작성해야할 API
- Django 는 요청 url 끝에 / 붙여줘야 합니다.. 련약한 장고..
    - 연결 확인 된 API 에 스티커 달아놔주면 땡큐베리감삼다~

- **접근 권한**에 대해서 Headers 설정은 다음처럼 해주심 됩니당

```python
AlloAny : 누구든 접근 가능
IsAuthenticated : 접근 권한 필요
				headers: { Authorization: `JWT ${token}` }  
```

## Swagger

- GET `swagger/`  👌 ㅋㅋㅋㅋㅋㅋㅋ

## User

- POST `user/login/`  로그인 👌
    - JWT 인증 토큰
    - AllowAny
    - Request

        ```python
        {
          "username": "string",
          "password": "string"
        }
        ```

    - Response

        ```python
        {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InRlc3RlcmpheSIsImV4cCI6MTU5MDU0NjM4NCwiZW1haWwiOiJ0dHRlc3RlckBhZy5jb20iLCJvcmlnX2lhdCI6MTU4OTk0MTU4NH0.DP5TBNaDENMCxS2gSxZouOQimsziUZAthvoMeR68rSo"
        }
        ```

- POST `user/`  회원가입 👌
    - 회원가입
    - AllowAny
    - Request
        - get_agreement 는 회원가입시 필수 입력 사항이 아니게 만들어두었읍니다. default=false

        ```python
        {
          "username": "string",
          "password": "string",
          "get_agreement": true, (0 or 1 가능, boolean field)
          "email": "user@example.com"
        }
        ```

    - Response
        - 200 - 'message': '회원가입 되었습니다.'
        - 400 - serializer error 에 따라서 이런저런 경우

            ```
            ex1)
            {
                "username": ["user의 username은/는 이미 존재합니다."]
            }

            ex2)
            {
            		"email": ["이 필드는 필수 항목입니다."]

            }

            ex3)
            {

                "username": ["user의 username은/는 이미 존재합니다."],

                "email": ["이 필드는 필수 항목입니다."],

            }
            ```

- GET  `user/login/rating/`  rating 5개 이상 했는지 확인하는 API 👌
    - IsAuthenticated (로그인 되어있어야 - header 에 담아보내는 방법 잠시만)
    - Response

        ```python
        지금까지 평가한 영화가 5개 이상이면 True 아니면 False

        { rating_tf: True/False}
        ```

- GET   user/taste/  영화취향 알기 위해서 영화 리스트 요청

- POST user/taste/  유저가 선택한 영화취향 별점 정보 입력
    - 

- GET  `user/` 마이페이지 들어갔을 때   **(진행 중)** 👌
    - IsAuthenticated
    - Response

        ```json
        {
            "id": 9000000,
            "username": "mrWoo0",
            "file": [
                "media/profile/202005262135276053.jpeg"
            ],
            "pick_movies": [],
            "pick_cinemas": []
        }
        ```

- POST  `user/profile/`  프사 생성 및 변경하기 👌
    - IsAuthenticated
    - 생성 및 수정이 둘 다 같은 API 입니당! 형태도 같아요! 걍 새 image를 POST 만 해주면 됨!!
    - 사용자가 아직 이미지 등록 안 한 경우 기본 이미지는 제 쪽에서 갖구 있을까요 지금처럼 지선이 만들어놓은 이미지로 해놓을까욥? 우리 회원가입 때 이미지 안 받으니까 기본 이미지가 있는거라고 생각했거든욥
    - Request

        ```json
        "Content-Type": "multipart/form-data"

        {"file": file}
        ```

    - Response

        ```json
        {
            "file": "media/profile/202005262135276053.jpeg"
        }

        src 예시: http://localhost:8000/media/profile/202005262135276053.jpeg
        ```

    - ER

        ```
        파일 형식이 문제있는 경우
        - status=400, {'message': '유효하지 않은 파일입니다.'}

        이미지 파일을 첨부하지 않은 경우
        - status=403, {'message': '이미지는 필수입니다.'}
        ```

- DELETE `user/profile/`  프사 삭제하기 👌
    - IsAuthenticated
    - Return

        ```json
        204  --- data X
        ```

- PATCH  `user/password/`   비번 변경하기 👌
    - IsAuthenticated
    - Request

        ```json
        {
           "~~password": '1234',~~
           "new_password": '5678'
        }
        ```

    - Response

        ```json
        203  --- data X
        ```

    - Error

        ```json
        status=400  {'message': '필수 데이터가 누락되었습니다.'}
        status=403  {'message': '비밀번호가 일치하지 않습니다.'}
        ```

## Home

- GET `cinema/map/`   위치 기반 주변 영화관 조회   👌
    - AllowAny
    - Request
        - query params
            - 필수 : x1, ,x2, y1, y2
            - 방식은 기존이랑 똑같아용
            - 기존의 x, y 중심좌표만 보내던건 일단 남겨둠: cinema/map/center/
            - ~~옵션: radius (default 1km)  — radius 를 어케 할지 함 논의 필요~~
            - x = 127.033311 = 'longitude' = '경도'
            - y = 37.5611326 = 'latitude' = '위도'

        ```python
        ~~http://localhost:8000/movie/cinema/map/?x=127.033311&y=37.5611326~~
        https://wouldyouci.ga/cinema/map/?x1=127.033311&y1=37.5611326&x2=127.033312&y2=37.5611327
        ```

    - Response

        ```python
        {
            "meta": {
                "total": 1  --- doc 개수
            },
            "documents": [
                {
                    "id": 47,  --- 더 주었으면 정보가 있다면 말씀해주세용 (글 하단 모델 참고)
                    "name": "메가박스 코엑스",
                    "type": "메가박스",
                    "img": "https://image2.megabox.co.kr/mop/home/appbunpage/URLVIEW.jpg",
                    "address": "서울 강남구 영동대로 513",
                    "tel": "1544-0070",
                    "x": "127.058215118259",
                    "y": "37.5130779481089",
                    "url": "https://www.megabox.co.kr/theater/time?brchNo=1351"
                }
            ]
        }
        ```

- GET `cinema/map/<int:cinema_id>/movie/`  상영중인 영화 빠른 시간 순 정렬 👌
    - AllowAny
    - queryparams
        - 필수 X
        - 옵션: date, start_time  (default = 오늘, 현재 시간)
            - date는 당일 기준 3일만 제공 (오늘이 수요일이면 수, 목 금)
            - 실시간 잔여좌석수는 일단 당일 것 만 제공
    - Request
        - id 1번하고 31번 (강남 CGV, 강남 메가박스) 데이터 있어용

        ```json
        http://localhost:8000/cinema/map/31/movie/
        http://localhost:8000/cinema/map/31/movie/?start_time=18:00
        ```

    - Response  — 먼가 더 필요하다, 넣자 싶은 데이터가 있다면 알려주세용

        ```json
        {
            "meta": {
                "total": 1
            },
            "documents": [
                {
                    "movie": {
                        "id": 129095,
                        "name": "지오스톰",
                        "poster": "https://movie-phinf.pstatic.net/20170922_133/1506059018478U7ur6_JPEG/movie_image.jpg",
                        "genres": [
                            "느와르",
                            "액션",
                            "무협"
                        ],
                        "running_time": "109분",
                        "watch_grade": "12세 관람가"
                    },
                    "info": "3관",
                    "date": "2020-05-25",
                    "start_time": "18:30:00",
                    "end_time": "20:00:00",
                    "total_seats": "53",
                    "seats": "14",
                    "url": "https://www.megabox.co.kr/booking/seat?playSchdlNo=2005251372021"
                }
            ]
        }
        ```

## Search

### 영화관 및 영화 상세정보에 나중에 total rating 하나 추가 할게욥

- GET  search/   검색페이지 들어갔을 때

- GET  search/movie/   영화 검색
- GET  search/cinema/  영화관 검색

- GET  `cinema/<int:cinema_id>/`   영화관 상세정보
    - IsAuthenticated
    - Response
        - 총 세 파트
        - 영화관 | 상영중인영화 | 댓글

        ```json
        {
            "id": 1,
            "name": "CGV강남",
            "type": "CGV",
            "img": "http://img.cgv.co.kr/Theater/Theater/2014/1211/CGVgangnam.jpg",
            "address": "서울 강남구 강남대로 438",
            "url": "http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0056",
            "tel": "1544-1122",
            "public": "# 지하철\n2호선 | 강남역 11번 출구\n9호선 | 신논현역 5번출구\n\n# 버스\n- 분당지역\n   좌석버스: 1005-1, 1005-2, 6800, 5500-2\n   간선버스: 408, 462\n   광역버스: 9404, 9408\n- 강북지역\n   간선버스: 140, 144, 145, 471\n- 강서지역\n   좌석버스: 1500\n   간선버스: 360\n- 강동지역\n   간선버스: 402, 420, 470, 407\n- 인근경기지역\n   좌석버스: 3030, 2002, 2002-1\n   광역버스: 9409, 9500, 9501, 9503, 9700, 9711",
            "parking": "# 주차정보\n- 위치: 건물 지하2F ~ 지하4F\n\n# 주차요금\n- CGV 영화 관람 시 주차 3시간 6,000원\n- 주차시간 (3시간) 초과 시 10분 당 1,000원\n※ 발렛서비스 운영시간 : 오전 8시 이후 ~ 오후 20시\n※ 발렛 무료 서비스는 영화 관람 고객 한 함.  (영화 미관람 시 건물 주차장에서 별도 정산)\n※ 20시 이후 입차 차량은 발렛서비스 이용이 제한될 수 있으며, 별도 운영되는 주차팀의 사정에 따라 변경될 수 있습니다.\n\n# 이용안내\n- 주차공간이 협소하여 평일 오후/주말은 주차가 어렵습니다.\n- 편리한 대중교통 이용을 이용하여 주시기 바랍니다.",
            "onscreens": [
                {
                    "movie": {
                        "id": 85579,
                        "name": "신과함께-죄와 벌",
                        "poster": "https://movie-phinf.pstatic.net/20171201_181/1512109983114kcQVl_JPEG/movie_image.jpg",
                        "genres": [
                            "판타지",
                            "서부"
                        ],
                        "running_time": "139분",
                        "watch_grade": "12세 관람가"
                    },
                    "info": "2관 | 3D",
                    "date": "2020-05-27",
                    "start_time": "05:00:00",
                    "end_time": "08:00:00",
                    "total_seats": "521",
                    "seats": "24",
                    "url": "https://www.megabox.co.kr/booking/seat?playSchdlNo=2005251372021"
                },
            ],
            "cinema_ratings": [
                {
                    "id": 1,
                    "comment": "blah",
                    "score": 5,
                    "updated_at": "2020-05-27T12:31:13.702559+09:00",
                    "user": {
                        "id": 9000000,
                        "username": "mrWoo0"
                    }
                }
            ]
        }
        ```

- GET  `cinema/<int:cinema_id>/pick/`    자주가는 영화관 등록 토글
    - IsAuthenticated
    - Response

        ```json
        {
            "pick_cinemas": true
        }
        ```

- POST  `cinema/rating/`    영화관 리뷰 남기기
    - IsAuthenticated
    - Request
    - Response

        ```json
        {
            "id": 1,
            "comment": "blah",
            "cinema": 1,
            "score": 5,
            "created_at": "2020-05-27T12:31:13.702559+09:00",
            "updated_at": "2020-05-27T12:31:13.702559+09:00"
        }
        ```

    - Error
        - 400

        ```json
        {
            "cinema": [
                "이 필드는 필수 항목입니다."
            ]
        }

        {
            "score": [
                "이 필드는 필수 항목입니다."
            ],
            "cinema": [
                "유효하지 않은 pk \"999\" - 객체가 존재하지 않습니다."
            ]
        }
        ```

- PATCH  `cinema/rating/<int:rating_id>/`   영화관 리뷰 수정하기
    - IsAuthenticated
    - Request

        ```json
        http://localhost:8000/user/cinema/rating/1/

        {
        	"comment": 'testest2',
          "score": 5,
          "cinema": 1
        }
        ```

    - Response

        ```json
        {
            "id": 2,
            "user": {
                "id": 9000000,
                "username": "mrWoo0"
            },
            "comment": "testest",
            "score": 5,
            "created_at": "2020-05-26T12:35:09.323348+09:00",
            "updated_at": "2020-05-26T12:39:03.941535+09:00",
            "cinema": 1
        }
        ```

    - POST 요청과 마찬가지로 필수 항목 - cinema, score 를 보내지 않으면 400

        ```json
        {
            "cinema": [
                "이 필드는 필수 항목입니다."
            ]
        }
        ```

    - rating 작성자 user_id 와 요청을 보낸 user_id가 일치하지 않으면 400

        ```json
        {
            "message": "권한이 없습니다."
        }
        ```

- DELETE  `cinema/rating/<int:rating_id>/`  영화관 리뷰 삭제하기
    - IsAuthenticated
    - Request
    - Response

        ```json
        204 --- data 없음
        ```

    - PATCH 와 마찬가지로 작성자와 요청자가 일치하지 않으면 400

- GET `movie/<int:movie_id>/`  영화 상세정보   👌❓
    - IsAuthenticated
    - is_showing 이 추가 되었습니다. 상영중(예매가능)이면 is_showing: true
        - 추가기능을 한다면, 상영중이면 → 버튼을 클릭하면 모달로 예매 할 수 있는 시간, 사이트 간단하게 띄워주면 어떨까 해요
    - id 아니고 movie_id 입니다!!! 달라도 상관은 없는거로 알긴하는데.. 혹시 모르니까!!
    - Response

        ```json
        {
        	"is_showing": true,
          "id": 152691,
          "name": "레이니 데이 인 뉴욕",
          "name_eng": "A Rainy Day in New York",
          "watch_grade": "15세 관람가",
          "running_time": "92분",
          "summary": "상상해 봐요 \n막 떨어지기 시작한 빗방울 \n센트럴 파크 델라코트 시계 아래 \n누군가 당신을 기다리고 있다면…\n재즈를 사랑하는 ‘개츠비’(티모시 샬라메)\n 영화에 푹 빠진 ‘애슐리’(엘르 패닝)\n 낭만을 꿈꾸는 ‘챈’(셀레나 고메즈)\n 매력적인 세 남녀가 선사하는 낭만적인 하루!\n \n 운명 같은 만남을 기대하며\n 봄비 내리는 뉴욕에서\n 로맨틱한 하루를 함께 하실래요?",
          "open_date": "2020-05-06",
          "trailer": "https://www.youtube.com/embed/yIVRldiVDL8",
          "poster": "https://movie-phinf.pstatic.net/20200417_176/1587098239671MiQEL_JPEG/movie_image.jpg",
          "directors": [
            "우디 앨런"
          ],
          "genres": [
            "모험"
          ],
          "actors": [
            "주드 로",
            "리브 슈라이버",
            "엘르 패닝",
            "셀레나 고메즈",
            "티모시 샬라메"
          ],
          "ratings": [
            {
              "id": 16859921,
              "comment": "여러분 불매합시다. 이 영화는 영화감독이 양녀 성추행으로 제작 국가인 북미에서도 개봉하지 못 했으며 주연인 티모시와 몇몇 다른 배우들은 이 영화 출연을 후회한다며 출연료 전액 기부하였습니다.불매해주셨으면 좋겠습니다. ",
              "score": 0,
              "updated_at": "2020-05-18T15:22:06.570000+09:00",
              "user": {
                "id": 9000000,
                "username": "mrWoo0"
              }
            },
            {
              "id": 216859931,
              "comment": "배우들도 개봉반대한 병크 감독 ㅋ",
              "score": 0,
              "updated_at": "2020-05-18T15:22:06.570000+09:00",
              "user": {
                "id": 9000002,
                "username": "mrWoo2"
              }
            },
            {
              "id": 116861165,
              "comment": "40살 차이나는 한국계 양딸을 미성년자 때부터 성추행한 감독 우디 앨런의 영화입니다. 전세계적으로 논란이 되어서 미국에서도 개봉이 취소되었는데 이걸 한국에서 개봉하다니요? 배우들도 후회된다며 출연료를 전액 기부했는데요? 수입사 그린나래미니어는 돈에 눈이 멀어서 아동성범죄자 감독의 영화를 홍보하나요? 진짜 더럽고 음침하고 추잡하네요. 부끄러운 줄 알아라! ",
              "score": 0,
              "updated_at": "2020-05-18T15:22:06.570000+09:00",
              "user": {
                "id": 9000001,
                "username": "mrWoo1"
              }
            }
          ]
        }
        ```

- PATCH  `movie/<int:movie_id>/pick/`    보고싶은 영화 등록 토글
    - IsAuthenticated
    - request
    - response

        ```json
        {
            "pick_movies": true
        }
        ```

- POST  `movie/rating/`    영화 리뷰 남기기   Response 일부 수정(user 안 가욥)
    - IsAuthenticated
    - Request

        ```json
        {
        	"comment": 'text',
          "score": 5,
          "movie": 152691  ---movie id
        }
        ```

    - Response

        ```json
        {
            "id": 216859940,
            "comment": "blah",
            "movie": 85579,
            "score": 5,
            "created_at": "2020-05-27T12:27:56.211048+09:00",
            "updated_at": "2020-05-27T12:27:56.211048+09:00"
        }
        ```

    - comment 는 필수가 아니지만 score, movie 정보가 누락되거나 없는 movie_id 를 제출하면 400 error

        ```json
        {
            "movie": [
                "이 필드는 필수 항목입니다."
            ]
        }

        {
            "score": [
                "이 필드는 필수 항목입니다."
            ],
            "movie": [
                "유효하지 않은 pk \"1\" - 객체가 존재하지 않습니다."
            ]
        }
        ```

- PATCH  `movie/rating/<int:rating_id>/`   영화 리뷰 수정하기
    - IsAuthenticated
    - Request

        ```json
        http://localhost:8000/user/movie/rating/216859933/

        {
        	"comment": 'testest2',
          "score": 5,
          "movie": 85579
        }
        ```

    - Response

        ```json
        {
            "id": 216859933,
            "user": {
                "id": 9000000,
                "username": "mrWoo0"
            },
            "comment": "testest2",
            "score": 5,
            "created_at": "2020-05-26T12:35:09.323348+09:00",
            "updated_at": "2020-05-26T12:39:03.941535+09:00",
            "movie": 85579
        }
        ```

    - POST 요청과 마찬가지로 필수 항목 - movie, score 를 보내지 않으면 400

        ```json
        {
            "movie": [
                "이 필드는 필수 항목입니다."
            ]
        }
        ```

    - rating 작성자 user_id 와 요청을 보낸 user_id가 일치하지 않으면 400

        ```json
        {
            "message": "권한이 없습니다."
        }
        ```

- DELETE  `movie/rating/<int:rating_id>/`   영화 리뷰 삭제하기
    - IsAuthenticated
    - Request
    - Response

        ```json
        204 --- data 없음
        ```

    - PATCH 와 마찬가지로 작성자와 요청자가 일치하지 않으면 400

  + back 단에서 해야할 일

- 영화 평점 만들고 수정하는 주기 설정하기
- 개봉예정작
- 백과 push 알람의 관계

---

---

# Model

1. User
2. Movie

    ```python
    {
        "id": 85579,
        "directors": [
          "김용화"
        ],
        "genres": [
          "판타지",
          "서부"
        ],
        "actors": [
          "차태현",
          "하정우",
          "김동욱",
          "주지훈",
          "김향기"
        ],
        "name": "신과함께-죄와 벌",
        "name_eng": "Along With the Gods: The Two Worlds",
        "watch_grade": "12세 관람가",
        "running_time": "139분",
        "summary": "저승 법에 의하면, 모든 인간은 사후 49일 동안 7번의 재판을 거쳐야만 한다. 살인, 나태, 거짓, 불의, 배신, 폭력, 천륜 7개의 지옥에서 7번의 재판을 무사히 통과한 망자만이 환생하여 새로운 삶을 시작할 수 있다.   “김자홍 씨께선, 오늘 예정 대로 무사히 사망하셨습니다”  화재 사고 현장에서 여자아이를 구하고 죽음을 맞이한 소방관 자홍, 그의 앞에 저승차사 해원맥과 덕춘이 나타난다. 자신의 죽음이 아직 믿기지도 않는데 덕춘은 정의로운 망자이자 귀인이라며 그를 치켜세운다. 저승으로 가는 입구, 초군문에서 그를 기다리는 또 한 명의 차사 강림, 그는 차사들의 리더이자 앞으로 자홍이 겪어야 할 7개의 재판에서 변호를 맡아줄 변호사이기도 하다. 염라대왕에게 천년 동안 49명의 망자를 환생시키면 자신들 역시 인간으로 환생시켜 주겠다는 약속을 받은 삼차사들, 그들은 자신들이 변호하고 호위해야 하는 48번째 망자이자 19년 만에 나타난 의로운 귀인 자홍의 환생을 확신하지만, 각 지옥에서 자홍의 과거가 하나 둘씩 드러나면서 예상치 못한 고난과 맞닥뜨리는데…  누구나 가지만 아무도 본 적 없는 곳, 새로운 세계의 문이 열린다!",
        "open_date": "2017-12-20",
        "trailer": "https://www.youtube.com/embed/sD7dmu-IWNw",
        "poster": "https://movie-phinf.pstatic.net/20171201_181/1512109983114kcQVl_JPEG/movie_image.jpg"
     }
    ```

3. Cinema

    ```python
    {
    			"region": "서울",
    			"area": "강남구",
    			"name": "CGV강남",
    			"code": "0056",
    			"tel": "1544-1122",
    			"address": "서울 강남구 강남대로 438",
    			"x": "127.026391177132",
    			"y": "37.5016573944824",
    			"url": "http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0056",
    			"public": "# 지하철\n2호선 | 강남역 11번 출구\n9호선 | 신논현역 5번출구\n\n# 버스\n- 분당지역\n   좌석버스: 1005-1, 1005-2, 6800, 5500-2\n   간선버스: 408, 462\n   광역버스: 9404, 9408\n- 강북지역\n   간선버스: 140, 144, 145, 471\n- 강서지역\n   좌석버스: 1500\n   간선버스: 360\n- 강동지역\n   간선버스: 402, 420, 470, 407\n- 인근경기지역\n   좌석버스: 3030, 2002, 2002-1\n   광역버스: 9409, 9500, 9501, 9503, 9700, 9711",
    			"parking": "# 주차정보\n- 위치: 건물 지하2F ~ 지하4F\n\n# 주차요금\n- CGV 영화 관람 시 주차 3시간 6,000원\n- 주차시간 (3시간) 초과 시 10분 당 1,000원\n※ 발렛서비스 운영시간 : 오전 8시 이후 ~ 오후 20시\n※ 발렛 무료 서비스는 영화 관람 고객 한 함.  (영화 미관람 시 건물 주차장에서 별도 정산)\n※ 20시 이후 입차 차량은 발렛서비스 이용이 제한될 수 있으며, 별도 운영되는 주차팀의 사정에 따라 변경될 수 있습니다.\n\n# 이용안내\n- 주차공간이 협소하여 평일 오후/주말은 주차가 어렵습니다.\n- 편리한 대중교통 이용을 이용하여 주시기 바랍니다.",
    			"type": "CGV",
    			"img": "http://img.cgv.co.kr/Theater/Theater/2014/1211/CGVgangnam.jpg"
    		}
    ```