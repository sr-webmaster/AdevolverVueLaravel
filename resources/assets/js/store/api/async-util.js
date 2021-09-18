import axios from 'axios'
import mutations from '../modules/accounts/mutations'

const doAsync = (commit, { url, mutationTypes, callback }) => {
  commit(mutationTypes.BASE, { type: mutationTypes.PENDING, value: true })

  return axios(url, {})
    .then(response => {
      const data = callback ? callback(response) : response
      commit(mutationTypes.BASE, { type: mutationTypes.SUCCESS, data, statusCode: response.status })
      commit(mutationTypes.BASE, { type: mutationTypes.PENDING, value: false})
    })
    .catch(error => {
      commit(mutationTypes.BASE, { type: mutationTypes.PENDING, value: false })
      commit(mutationTypes.BASE, { type: mutationTypes.FAILURE, statusCode: error.response.status })
    })
}
export default doAsync
