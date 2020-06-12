<template>
  <div>
      <Title />
    <v-dialog v-model="timeSelector">
      <TimeSelector v-bind:nowTime="time" @targetTime="changeTime"/>
    </v-dialog>
    <div id="map" ref="map">
    </div>
    <v-overlay :value="getLoading">
        <v-progress-circular
                :size="70"
                :width="7"
                color="#4520EA"
                indeterminate
        />
    </v-overlay>
      <v-toolbar
              dense
              floating
              width="90vw"
              class="myToolbar"
      >
        <div class="v-toolbar__content">
          <v-text-field @click="timeSelector=!timeSelector"
            hide-details
            single-line
            v-bind:label="timeForUser"
            prepend-icon="search"
          />

          <v-btn icon>
            <v-icon
              color="lightpink"
              @click="setNowTime">mdi-history</v-icon>
          </v-btn>

          <v-btn icon>
              <v-icon
                v-if="isLoggedIn"
                color="blackpink"
                @click="goUserPage">mdi-account-circle</v-icon>
              <v-icon
                v-else
                color="lightpink"
                @click="goUserPage">mdi-account-circle</v-icon>
          </v-btn>
        </div>
      </v-toolbar>

    <div v-if="isChangeLocation">
      <v-btn small class="nowArea" v-if="loading" loading>
        <v-icon small class="btnIcon" left>fas fa-undo-alt</v-icon> 주변 시네마 검색
      </v-btn>
      <v-btn small class="nowArea" color="rgba(255, 255, 255, 0.8)" @click="changeLoading" v-else>
        <v-icon small class="btnIcon" left>mdi-map-search-outline</v-icon> 여기 주변 시네마
      </v-btn>
    </div>

    <div class="movieCard" v-if="showMovieCard">
      <TheaterMovie v-bind:theaterType="theaterType" v-bind:theaterId="theaterId" v-bind:theaterName="theaterName" v-bind:theaterMovieList="getMovies"/>
    </div>
      <div v-else>
          <v-btn class="reload" @click="findMyPos" fab height="30" width="30">
              <v-icon small color="lightprimary">fas fa-crosshairs</v-icon>
          </v-btn>
      </div>
  </div>
</template>

<script>
  import router from "@/router";
import Title from '../nav/Title.vue';
import TimeSelector from './timeSelector/TimeSelector.vue';
import TheaterMovie from './theaterMovie/TheaterMovie.vue';
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default {
  name: 'MainMap',
  components: {
    Title,
    TimeSelector,
    TheaterMovie
  },
  data() {
    return {
      map: null,
      google: null,
      nowHere: null,
      time: new Date(),
      timeForUser: null,
      isTimeChange: false,
      cardInfo: null,
      showMovieCard: null,
      loading: false,
      mapBound: null,
      timeSelector: false,
      theaterMovieList: [],
      markers: [],
      cgvMarkers: [],
      megaMarkers: [],
      lotMarkers: [],
      theaterId: null,
      theaterName: null,
      theaterType: null,
      isChangeLocation: false,
      myMarker: null,
      infowindows:[],
      HOST:process.env.VUE_APP_SERVER_HOST
    }
  },
  computed: {
    ...mapGetters(['getTheaterMovies', 'getMovies', 'getLoading', 'isLoggedIn'])

  },
  methods: {
    ...mapMutations(['setLoading', 'setLoginMode']),
    ...mapActions(['init', 'bringHereCinema', 'bringMovies']),
    goUserPage() {
      if (this.isLoggedIn) {
        const link = document.location.href.split("/");
        if (link[link.length - 1] !== "userPage") {
          router.push('/userPage');
        } else {
          location.reload();
        }
      } else {
        this.setLoginMode('login');
        router.push('/signup');
      }
    },
    marking(value) {
      // const HOST = process.env.VUE_APP_SERVER_HOST;
      if (value.type === 'user') {
        const marker = new this.google.maps.Marker({position: value.position, map: this.map, icon: value.icon})
        this.myMarker = marker;
        this.google.maps.event.addListener(marker, 'click', function() {
          if (this.showMovieCard) {
            this.closeMovieCard();
          }
          const infoWindow = new window.google.maps.InfoWindow;
          infoWindow.setPosition({lat: value.position.lat, lng: value.position.lng});
          infoWindow.setContent('현재 위치입니다. 실제 위치와 500m 정도 차이가 날 수 있습니다.');
          infoWindow.open(this.map);
          this.infowindows.push(infoWindow);
        }.bind(this))
      } else {
        if (value.position.length) {
          const zoomLevel = this.map.getZoom();
          for (const v of value.position) {
            let theaterIcon = {
              url: `${this.HOST}/media/wouldyouci/wouldyouci.png`,
              scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
            }
            if (v.type === 'CGV') {
              theaterIcon = {
                url: `${this.HOST}/media/wouldyouci/cgv.png`,
                scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
              }
            } else if (v.type === '메가박스') {
              theaterIcon = {
                url: `${this.HOST}/media/wouldyouci/megabox.png`,
                scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
              }
            } else if (v.type === '롯데시네마') {
              theaterIcon = {
                url: `${this.HOST}/media/wouldyouci/lotte.png`,
                scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
              }
            }
            const marker = new this.google.maps.Marker({position: {lat: Number(v.y), lng: Number(v.x)}, map: this.map, icon: theaterIcon, animation: this.google.maps.Animation.DROP})
            if (v.type === 'CGV') {
              this.cgvMarkers.push(marker);
            } else if (v.type === '메가박스') {
              this.megaMarkers.push(marker);
            } else if (v.type === '롯데시네마') {
              this.lotMarkers.push(marker);
            } else {
              this.markers.push(marker);
            }
            this.google.maps.event.addListener(marker, 'click', async function() {
              this.theaterId = v.id;
              this.theaterName = v.name;
              this.theaterType = v.type;
              this.setLoading(true);
              if (this.isTimeChange) {
                await this.bringMovies({theaterID: v.id, time: this.time});
              } else {
                await this.bringMovies({theaterID: v.id, time: null});
              }
              this.setLoading(false);
              if (this.cardInfo && this.cardInfo !== marker) {
                this.showMovieCard = false;
                this.toggleBounce(this.cardInfo);
                this.toggleBounce(marker);
                this.cardInfo = marker;
                setTimeout(function() {
                  this.showMovieCard = true;
                }.bind(this), 1)
              } else if (!this.cardInfo) {
                this.toggleBounce(marker);
                this.cardInfo = marker;
                this.showMovieCard = true;
              }
            }.bind(this))
          }
        }
        else{
          alert('해당 지역에는 영화관이 없습니다.\n지역을 다시 설정해주세요.')
        }
      }
    },
    handleLocationError(browserHasGeolocation, pos) {
      const infoWindow = new window.google.maps.InfoWindow;
      infoWindow.setPosition(pos);
      infoWindow.setContent(browserHasGeolocation?
                              '오류: 지리적 위치 서비스가 실패했습니다. 위치 제공을 허용해주세요':
                              '오류: 브라우저가 지리적 위치를 지원하지 않습니다.');
      infoWindow.open(this.map);
      this.infowindows.push(infoWindow);
      if (browserHasGeolocation) {
        alert('위치 정보 제공에 동의해주세요.')
      } else {
        alert('브라우저가 지리적 위치를 지원하지 않습니다.')
      }
    },
    toggleBounce(marker) {
      if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
        this.cardInfo = null;
      } else {
        marker.setAnimation(window.google.maps.Animation.BOUNCE);
      }
    },
    closeMovieCard() {
      this.showMovieCard = false;
      this.toggleBounce(this.cardInfo);
    },
    getUserTime() {
      if (this.isTimeChange) {
        const temp = this.time.split(' ');
        const amPm = temp[0];
        const hours = temp[1].split(':')[0];
        const mins = temp[1].split(':')[1];
        this.timeForUser = `${amPm} ${hours}시 ${mins}분 기준 영화`;
      } else {
        let hours = this.time.getHours();
        let mins = this.time.getMinutes();
        const amPm = hours >= 12 ? '오후' : '오전';
        hours = hours % 12;
        hours = hours ? hours : 12;
        mins = mins < 10 ? `0${mins}` : mins;
        this.timeForUser = `${amPm} ${hours}시 ${mins}분 기준 영화`;
      }
    },
    async changeLoading() {
      this.loading = true;
      this.clearMarker();
      const mapBound = this.map.getBounds();
      this.mapBound = mapBound;
      const bound = {
        x1: mapBound.Ua.i,
        y1: mapBound.Ya.i,
        x2: mapBound.Ua.j,
        y2: mapBound.Ya.j
      }
      await this.bringHereCinema(bound);
      this.theaterMovieList = this.getTheaterMovies;
      this.marking({type: 'theater', position: this.theaterMovieList});
      this.isChangeLocation = false;
      this.loading = false;
    },
    async changeTime(targetTime) {
      this.timeSelector = false;
      const targetTimes = targetTime.split(' ');
      const times = targetTimes[1].split(':');
      if (targetTimes[0] !== 'null' && times[0] !== 'null' && times[1] !== 'null') {
        this.isTimeChange = true;
        this.time = targetTime;
        this.getUserTime();
        if (this.showMovieCard) {
          this.showMovieCard = false;
          setTimeout(function() {
            this.showMovieCard = true;
          }.bind(this), 1);
          this.setLoading(true);
          await this.bringMovies({theaterID: this.theaterId, time: this.time});
          this.setLoading(false);
        }
      }
    },
    async setNowTime() {
      this.time = new Date();
      this.isTimeChange = false;
      this.getUserTime();
      if (this.showMovieCard) {
        this.setLoading(true);
        await this.bringMovies({theaterID: this.theaterId, time: null});
        this.setLoading(false);
      }
    },
    clearMarker() {
      for (const marker of this.markers) {
        marker.setMap(null);
      }
      for (const marker of this.cgvMarkers) {
        marker.setMap(null);
      }
      for (const marker of this.megaMarkers) {
        marker.setMap(null);
      }
      for (const marker of this.lotMarkers) {
        marker.setMap(null);
      }
      for (const infowindow of this.infowindows) {
        infowindow.close();
      }
    },
    findMyPos() {
      this.isChangeLocation = false;
      this.clearMarker();
      if (this.myMarker) {
        this.myMarker.setMap(null);
      }
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async function(position) {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          this.map.setCenter(pos);
          const mapBound = this.map.getBounds();
          this.mapBound = mapBound;
          const bound = {
            x1: mapBound.Ua.i,
            y1: mapBound.Ya.i,
            x2: mapBound.Ua.j,
            y2: mapBound.Ya.j
          }
          await this.bringHereCinema(bound);
          this.theaterMovieList = this.getTheaterMovies;
          this.nowHere = pos;
          const hereIcon = {
            url : "https://k02a4061.p.ssafy.io/media/pin.svg",
            scaledSize: new this.google.maps.Size(40, 40)
          }
          this.marking({type: 'user', position: pos, icon: hereIcon});
          this.marking({type: 'theater', position: this.theaterMovieList});
        }.bind(this), function() {
          this.handleLocationError(true, this.map.getCenter());
        }.bind(this))
      } else {
        this.handleLocationError(false, this.map.getCenter());
      }
    }
  },
  async mounted() {
    this.setLoginMode(null);
    this.setLoading(true);
    this.getUserTime();
    try {
      this.google = await this.init();
      this.map = new this.google.maps.Map(this.$refs.map, {
        center: { lat: 37.501401, lng: 127.039686 },
        zoom: 14,
        disableDefaultUI: true
      });
      this.google.maps.event.addListener(this.map, 'click', function() {
        if (this.showMovieCard) {
          this.closeMovieCard();
        }
      }.bind(this))
      this.map.addListener('dragend', function() {
        this.isChangeLocation = true;
      }.bind(this))
      this.map.addListener('zoom_changed', function() {
        this.isChangeLocation = true;
        const zoomLevel = this.map.getZoom();
        for (const marker of this.markers) {
          marker.setIcon(
            {
              url: `${this.HOST}/media/wouldyouci/wouldyouci.png`,
              scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
            }
          );
        }
        for (const marker of this.cgvMarkers) {
          marker.setIcon(
            {
              url: `${this.HOST}/media/wouldyouci/cgv.png`,
              scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
            }
          );
        }
        for (const marker of this.megaMarkers) {
          marker.setIcon(
            {
              url: `${this.HOST}/media/wouldyouci/megabox.png`,
              scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
            }
          );
        }
        for (const marker of this.lotMarkers) {
          marker.setIcon(
            {
              url: `${this.HOST}/media/wouldyouci/lotte.png`,
              scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
            }
          );
        }
        this.myMarker.setIcon({
          url : "https://k02a4061.p.ssafy.io/media/pin.svg",
          scaledSize: new this.google.maps.Size(zoomLevel*3, zoomLevel*3)
        })
      }.bind(this))
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async function(position) {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          this.map.setCenter(pos);
          const bound = {x1: pos.lng - 0.01544952392, y1: pos.lat - 0.01721547104, x2: pos.lng + 0.01544952392, y2: pos.lat + 0.01721150239};
          await this.bringHereCinema(bound);
          this.theaterMovieList = this.getTheaterMovies;
          this.nowHere = pos;
          const hereIcon = {
            url : "https://k02a4061.p.ssafy.io/media/pin.svg",
            scaledSize: new this.google.maps.Size(14*3, 14*3)
          }
          this.marking({type: 'user', position: pos, icon: hereIcon});
          this.marking({type: 'theater', position: this.theaterMovieList});
          this.setLoading(false);
        }.bind(this), function() {
          this.handleLocationError(true, this.map.getCenter());
          this.setLoading(false);
        }.bind(this))
      } else {
        this.setLoading(false);
      }
    } catch (error) {
      this.handleLocationError(false, this.map.getCenter());
      this.setLoading(false);
    }
  }
}
</script>

<style src="./MainMap.css" scoped></style>
