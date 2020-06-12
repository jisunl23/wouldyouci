import router from "../../router";
const HOST = process.env.VUE_APP_SERVER_HOST;
const axios = require("axios");

const state = {
  LoginMode: null,
  token: null,
  errors: [],
  loading: false,
  userInfo: null
};

const getters = { 
  getLoginMode: state => state.LoginMode,
  isLoggedIn: state => !!state.token,
  getErrors: state => state.errors,
  getLoading: state => state.loading,
  getUserInfo: state => state.userInfo
};

const mutations = {
  setLoginMode: (state, type) => (state.LoginMode = type),
  setToken: (state, token) => {
    state.token = token;
    sessionStorage.setItem("jwt", token);
  },
  pushError: (state, error) => state.errors.push(error),
  clearErrors: state => state.errors = [],
  setLoading: (state, bool) => state.loading = bool,
  setUserInfo: (state, userInfo) => state.userInfo = userInfo
};

const actions = {
  initialLogin: ({ commit }) => {
    const token = sessionStorage.getItem("jwt");
    if (token) {
      commit("setToken", token);
    }
  },
  login: ({ getters, commit, dispatch }, userInfo) => {
    if (getters.isLoggedIn) {
      router.push("/");
    } else {
      commit("clearErrors");
      const data = {
        username: userInfo.userName,
        password: userInfo.password
      }
      const options = {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        }
      }
      if (!userInfo.userName && !userInfo.password) {
        commit("pushError", "아이디를 입력해주세요.")
        commit("pushError", "비밀번호를 입력해주세요.")
      } else if (!userInfo.password) {
        commit("pushError", "비밀번호를 입력해주세요.")
      } else if (!userInfo.userName) {
        commit("pushError", "아이디를 입력해주세요.")
      } else {
        commit('setLoading', true);
        axios.post(`${HOST}/user/login/`, data, options)
        .then(res => {
          commit('setLoading', false);
          commit("setToken", res.data.token);
          dispatch("checkRating", 'login');
        })
        .catch(err => {
          commit('setLoading', false);
          if (err.response && err.response.data.non_field_errors.length) {
            commit("pushError", "아이디 혹은 패스워드가 올바르지 않습니다.")
          }
        })
      }
    }
  },
  signup: ({ getters, commit, dispatch }, userInfo) => {
    if (getters.isLoggedIn) {
      router.push("/");
    }
    commit("clearErrors");
    if (!userInfo.userName && !userInfo.password && !userInfo.email) {
      commit("pushError", "아이디를 입력해주세요.")
      commit("pushError", "이메일을 입력해주세요.")
      commit("pushError", "비밀번호를 입력해주세요.")
    } else if (!userInfo.userName && !userInfo.password) {
      commit("pushError", "아이디를 입력해주세요.")
      commit("pushError", "비밀번호를 입력해주세요.")
    } else if (!userInfo.userName && !userInfo.email) {
      commit("pushError", "아이디를 입력해주세요.")
      commit("pushError", "이메일을 입력해주세요.")
    } else if (!userInfo.email && !userInfo.password) {
      commit("pushError", "이메일을 입력해주세요.")
      commit("pushError", "비밀번호를 입력해주세요.")
    } else if (!userInfo.userName) {
      commit("pushError", "아이디를 입력해주세요.")
    } else if (!userInfo.email) {
      commit("pushError", "이메일을 입력해주세요.")
    } else if (!userInfo.password) {
      commit("pushError", "비밀번호를 입력해주세요.")
    } else {
      if (userInfo.password !== userInfo.passwordConfirm) {
        commit("pushError", "비밀번호가 일치하지 않습니다.")
      } else {
        commit('setLoading', true);
        const data = {
          username: userInfo.userName,
          password: userInfo.password,
          email: userInfo.email
        }
        const options = {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
          }
        }
        axios.post(`${HOST}/user/signup/`, data, options)
          .then(res => {
            res;
            commit('setLoading', false);
            const credentials = {
              userName: userInfo.userName,
              password: userInfo.password
            }
            dispatch("login", credentials);
          })
          .catch(err => {
            commit('setLoading', false);
            if (err.response && err.response.data.message.username){
              for (let i=0; i<err.response.data.message.username.length; i++){
                if (err.response.data.message.username[i] === "user의 username은/는 이미 존재합니다.") {
                  commit("pushError", "이미 존재하는 아이디입니다.");
                } else if (err.response.data.message.username[i] === "이 필드의 글자 수가 20 이하인지 확인하십시오.") {
                  commit("pushError", "아이디는 20자 이하만 가능합니다.");
                } else {
                  commit("pushError", err.response.data.message.username[i]);
                }
              }
            }
            if (err.response && err.response.data.message.email) {
              for (let i=0; i<err.response.data.message.email.length; i++){
                commit("pushError", err.response.data.message.email[i]);
              }
            }
            if (err.response && err.response.data.message.password) {
              for (let i=0; i<err.response.data.message.password.length; i++) {
                commit("pushError", err.response.data.message.password[i]);
              }
            }
          })
      }
    }
  },
  logout: ({ commit }) => {
    commit("setToken", null);
    sessionStorage.removeItem("jwt");
    router.push("/signup");
  },
  checkRating: ({ commit }, type) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    }
    if (type === 'login') {
      axios.get(`${HOST}/user/login/rating/`, options)
        .then(res => {
          commit('setLoading', false);
          if (!res.data.rating_tf) {
            router.push('/firstRating');
          } else {
            router.push('/');
          }
        })
        .catch(err => {
          err;
        })
    } else {
      return new Promise(function(resolve, reject) {
        axios.get(`${HOST}/user/login/rating/`, options)
          .then(res => {
            resolve(res.data.rating_cnt);
          })
          .catch(err => {
            err;
            reject(Error('error'));
          })
      })
    }
  },
  changePassword: ({ getters }, userInfo) => {
    getters;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    };
    const data = {
      new_password: userInfo.password
    };
    axios.patch(`${HOST}/user/password/`, data, options)
      .then(res => {
        res;
        alert('비밀번호가 변경되었습니다.')
      })
      .catch(err => {
        err;
        alert('비밀번호를 변경하는데 오류가 발생하였습니다.')
      })
  },
  registerProfile: ({ getters }, image) => {
    getters;
    const data = new FormData();
    data.append('file', image);
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "multipart/form-data",
      }
    }
    return new Promise(function(resolve, reject) {
      axios.post(`${HOST}/user/profile/`, data, options)
        .then(res => {
          res;
          resolve('ok');
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
    })
  },
  deleteProfile: ({ getters }) => {
    getters;
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    };
    return new Promise(function(resolve, reject) {
      axios.delete(`${HOST}/user/profile/`, options)
        .then(res => {
          res;
          resolve('ok');
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
    })
  },
  bringUserInfo: ({ commit }) => {
    const token = sessionStorage.getItem('jwt');
    const options = {
      headers: {
        Authorization: `JWT ${token}`
      }
    };
    return new Promise(function(resolve, reject) {
      axios.get(`${HOST}/user/`, options)
        .then(res => {
          commit('setUserInfo', res.data)
          resolve('ok');
        })
        .catch(err => {
          err;
          reject(Error('error'));
        })
    })
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};