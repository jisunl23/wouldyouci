const axios = require("axios");

const instance = axios.create({
  baseURL: process.env.VUE_APP_SERVER_HOST,
  headers: {
    'Content-Type' : 'application/json',

  }
});


export function fetchMovie(id) {
  return instance.get(`/movie/${id}/`);
}

export function fetchCinema(id) {
  return instance.get(`/cinema/${id}/`);
}

export function postRating(rating) {
  return instance.post(`/movie/rating/`, rating);
}