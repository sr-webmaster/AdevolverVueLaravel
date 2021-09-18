import { Line, mixins } from 'vue-chartjs'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
Chart.plugins.register(ChartAnnotationsPlugin)
const { reactiveProp } = mixins

export default {
  extends: Line,
  props: {
    chartData: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  },
  watch: {
    options: {
      handler (newOption, oldOption) {
        this.renderChart(this.chartData, this.options)
      },
      deep: true
    }
  },
  mixins: [reactiveProp],
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
