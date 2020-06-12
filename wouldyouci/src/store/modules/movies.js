import router from "../../router";

const API_KEY = process.env.VUE_APP_GOOGLE_MAP_API_KEY;
const KAKAO_API_KEY = process.env.VUE_APP_KAKAO_API_KEY;
const HOST = process.env.VUE_APP_SERVER_HOST;
const axios = require("axios");

var resolveInitPromise;
var rejectInitPromise;

const initPromise = new Promise((resolve, reject) => {
  resolveInitPromise = resolve;
  rejectInitPromise = reject;
});

const state = {
  initialized: !!window.google,
  searchMode: "before",
  theaterMovies: [],
  movies: [],
  searchList: [],
  searchSimiList: [],
  initSearchInfo: null,
  address: null,

  movieDetail: [],
  movieRatings: [],
  cinemaDetail: [],
  cinemaRatings: [],
  movieShowingCinemas: [],
  avgScore: null,
};

const getters = {
  getInitialized: state => state.initialized,
  getSearchMode: state => state.searchMode,
  getTheaterMovies: state => state.theaterMovies,
  getMovies: state => state.movies,
  getSearchList: state => state.searchList,
  getSearchSimiList: state => state.searchSimiList,
  getInitSearchInfo: state => state.initSearchInfo,
  getAddress: state => state.address,

  getMovieDetail: state => state.movieDetail,
  getMovieRatings: state => state.movieRatings,
  getCinemaDetail: state => state.cinemaDetail,
  getCinemaRatings: state => state.cinemaRatings,
  getMovieShowingCinemas: state => state.movieShowingCinemas,
  getAvgScore: state => state.avgScore,
};

const mutations = {
  setInitialized: (state, value) => state.initialized = value,
  setSearchMode: (state, mode) => state.searchMode = mode,
  setTheaterMovies: (state, theaterMovies) => state.theaterMovies = theaterMovies,
  setMovies: (state, movies) => state.movies = movies,
  setNearTheater: (state, theaters) => state.nearTheater = theaters,
  setSearchList: (state, movies) => state.searchList = movies,
  setSearchSimiList: (state, movies) => state.searchSimiList = movies,
  setInitSearchInfo: (state, info) => state.initSearchInfo = info,
  setAddress: (state, address) => state.address = address,

  setMovieDetail: (state, details) => state.movieDetail = details,
  setMovieRatings: (state, ratings) => state.movieRatings = ratings,
  setCinemaDetail: (state, details) => state.cinemaDetail = details,
  setCinemaRatings: (state, ratings) => state.cinemaRatings = ratings,
  setMovieShowingCinemas: (state, cinemas) => state.movieShowingCinemas = cinemas,
  setAvgScore: (state, score) => state.avgScore = score,
};

const actions = {
  init: ({ getters, commit }) => {
    if (getters.getInitialized) return initPromise;
    commit("setInitialized", true);
    window["initMap"] = () => resolveInitPromise(window.google);
    const script = document.createElement("script");
    script.async = true;
    script.defer = true;
    script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&callback=initMap`;
    script.type="text/javascript"
    script.onerror = rejectInitPromise;
    document.querySelector("body").appendChild(script);
    return initPromise;
  },
  bringHereCinema: ({ commit }, bound) => {
    const params = {
      params: {
        x1: bound.x1,
        y1: bound.y1,
        x2: bound.x2,
        y2: bound.y2
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/cinema/map/`, params)
        .then(res => {
          commit('setTheaterMovies', res.data.documents);
          resolve('ok');
        })
        .catch(err => {
          err;
          reject(Error('error'))
        })
    })
  },
  bringMovies: ({ commit }, {theaterID, time}) => {
    let params = null;
    if (time) {
      const amPm = time.split(' ')[0];
      const times = time.split(' ')[1].split(':');
      let startH = null;
      if (amPm === '오전') {
        if (times[0] === '12') {
          startH = '24'
        } else {
          startH = '0'+times[0];
        }
      } else {
        if (times[0] === '12') {
          startH = times[0];
        } else {
          startH = String(Number(times[0])+12);
        }
      }
      params = {
        params: {
          start_time: `${startH}:${times[1]}`
        }
      };
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/cinema/map/${theaterID}/movie/`, params)
        .then(res => {
          commit('setMovies', res.data.documents);
          resolve('ok');
        })
        .catch(err => {
          err;
          reject(Error('error'))
        })
    })
  },
  searchMovies: ({ commit }, keywords) => {
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/search/movie/${keywords}/`)
        .then(res => {
          commit('setSearchList', res.data.search_result);
          commit('setSearchSimiList', res.data.similar_result);
          resolve(res.data);
        })
        .catch(err => {
          err;
          commit('setSearchList', null);
          commit('setSearchSimiList', null);
          reject(Error('error'));
        })
    })
  },
  searchTheater: ({ commit }, keywords) => {
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/search/cinema/${keywords}/`)
        .then(res => {
          commit('setSearchList', res.data.search_result);
          commit('setSearchSimiList', res.data.similar_result);
          resolve('ok');
        })
        .catch(err => {
          err;
          commit('setSearchList', null);
          commit('setSearchSimiList', null);
          reject(Error('error'));
        })
    })
  },
  bringAddress: ({ commit }, pos) => {
    if (pos) {
      const KOptions = {
        headers: {
          Authorization: `KakaoAK ${KAKAO_API_KEY}`
        }
      }
      return new Promise(function(resolve, reject) {
        axios.get(`https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=${pos.lng}&y=${pos.lat}`, KOptions)
        .then(res => {
          commit('setAddress', res.data.documents[0].address_name);
          resolve('ok')
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
      })
    } else {
      return new Promise(function(resolve) {
        commit('setAddress', '위치 정보를 허용해주세요.')
        resolve('ok');
      })
    }
  },
  bringInitSearchInfo: ({ commit }, pos) => {
    const token = sessionStorage.getItem('jwt');
    let options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    if (pos) {
      options = {
        headers: {
          Authorization: `JWT ${token}`
        },
        params: {
          x: pos.lng,
          y: pos.lat
        }
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/search/`, options)
      .then(res => {
        commit('setInitSearchInfo', res.data);
        resolve('ok');
      })
      .catch(err => {
        err;
        reject(Error('error'));
      })
    })
  },
  bringRatingMovies: ({ getters }, next) => {
    getters;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      },
      params: {
        page: next
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/user/rating/page/`, options)
        .then(res => {
          resolve(res.data);
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
    })
  },
  submitRatings: ({ getters }, movies) => {
    getters;
    let data = [];
    for (const [key, value] of Object.entries(movies)) {
      data.push({movie: key, score: value});
    }
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    axios.post(`${HOST}/user/rating/`, {data}, options)
      .then(res => {
        res;
        router.push('/');
      })
      .catch(err => {
        err;
      })
  },
  bringRatedMovies: ({ getters }) => {
    getters;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/user/rating/`, options)
        .then(res => {
          resolve(res.data);
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
    })
  },
  fetchMovieDetail: ({ commit }, movieId) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/movie/${movieId}/`, options)
        .then(res => {
          commit('setMovieDetail', res.data);
          resolve('ok')
        })
        .catch(err => {
          err;
          if ( err.response.status == 404) {
            router.push('/404')
          } else {
            reject(Error('error'))
          }
        })
    })
  },
  fetchCinemaDetail: ({ commit }, cinemaId) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/cinema/${cinemaId}/`, options)
        .then(res => {
          commit('setCinemaDetail', res.data);
          resolve('ok')
        })
        .catch(err => {
          err;
          if ( err.response.status == 404) {
            router.push('/404')
          } else {
            reject(Error('error'))
          }
        })
    })
  },
  togglePick: ({dispatch}, {item, itemId}) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
      }
    }
    axios.patch(`${HOST}/${item}/${itemId}/pick/`, 1, options)
      .then(res => {
        res;
        if ( item == 'cinema' ) {
          return dispatch('fetchCinemaDetail', itemId)
        } else {
          return dispatch('fetchMovieDetail', itemId);
        }
      })
      .catch(err => {
        err;
      })
  },
  fetchScore: ({ commit }, {item, itemId} ) => {
    commit;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
      },
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/${item}/${itemId}/score/`, options)
        .then(res => {
          commit('setAvgScore', res.data["score"])
          resolve(res.data)
        })
        .catch(err => {
          reject(err, Error('error'))
        })
    })
  },
  fetchRatings: ({ commit }, {item, params} ) => {
    commit;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
      },
      params: params
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/${item}/rating/page/`, options)
        .then(res => {
          resolve(res.data)
        })
        .catch(err => {
          reject(Error(err))
        })
    })
  },
  postRating: ({ dispatch }, {item, rating}) => {
    dispatch;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json",
      }
    }
    return new Promise(function(resolve, reject) {
      axios.post(`${HOST}/${item}/rating/`, rating, options)
        .then(res => {
          resolve(res);
        })
        .catch(err => {
          reject(Error('error'));
          if (err.response.status == 403) {
            alert('이미 리뷰를 작성하셨습니다.')
          }
        })
      })
  },
  delRating: ({dispatch}, {item, ratingId}) => {
    dispatch;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
      }
    }
    return new Promise(function(resolve, reject) {
      axios.delete(`${HOST}/${item}/rating/${ratingId}/`, options)
        .then(res => {
          resolve(res);
        })
        .catch(err => {
          reject(err);
        })
      })
  },
  patchRating: ({dispatch}, {item, editedRating}) => {
    dispatch;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json",
      }
    }
    return new Promise(function(resolve, reject) {
    axios.patch(`${HOST}/${item}/rating/${editedRating.id}/`, editedRating, options)
      .then(res => {
        resolve(res);
      })
      .catch(err => {
        err;
        reject(Error('error'));
      })
    })
  },
  fetchMovieShowingCinemas: ({ commit }, movieId) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/movie/${movieId}/onscreen/`, options)
        .then(res => {
          commit('setMovieShowingCinemas', res.data);
          resolve('ok')
        })
        .catch(err => {
          err;
          reject(Error('error'))
        })
    })
  },

  

};

export default {
  state,
  getters,
  mutations,
  actions
};