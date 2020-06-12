import 'material-design-icons-iconfont/dist/material-design-icons.css'
import "@fortawesome/fontawesome-free/css/all.css";
import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: "fa" || "md" || "mdi"
  },
  theme: {
    themes: {
      light: {
        primary: '#67247B',
        secondary: '#1d0840',
        accent: '#E91E63',
        error: '#b71c1c',
        lightprimary: '#674c80',
        lightpink:'#F692C1',
        mypink: '#F25CA2',
        blackpink: '#cd4e80',
        greypink: '#cfa8c4',
        clearBlue: '#0433BF',
        blue: '#032CA6',
        darkBlue:'#021859',
        lightBlue: '#91e2ff',
        grey: '#0D2C40',
        lightYellow: '#F2E6A7',
        yellow: '#F2CF63',
        lightPink:'#D9A796',
        white: '#fafafa',
        fontgrey: '#768285',
        elsepink: '#ff748f',
        megabox: '#672484',
        cgv: '#e32f57',
        lotte: '#f69a05',
        titlepink: '#fb9cb5',
        titleblue: '#6382ce',
      }
    },
  },
});
