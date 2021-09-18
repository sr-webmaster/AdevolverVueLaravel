export const namespaced = true

import DataState from '../../DataState';
import axios from 'axios'

let data_state = new DataState()

export default {
	state:{
    response_data:{},
    response:{},
    data_state: data_state,
    promise: {},
    notify_via_email: 0,
    pause_campaigns: 0,
    enable_campaigns: 0,
    rollover_spend: 0,
    control_spend: 0,
    excess_budget: 0,
    emergency_stop: 0,
    budget: 0,
    kpi_option: 'CPA',
    kpi_target: 0,
    groupList: []
  },
  getters: {
    budget_commander_response_data: state => state.response_data,
    budget_commander_response: state => state.response,
    budget_commander_data_state: state => state.data_state,
    budget_commander_promise: state => state.promise,
    budget_commander_pause_campaigns: state => state.pause_campaigns,
    budget_commander_enable_campaigns: state => state.enable_campaigns,
    budget_commander_rollover_spend: state => state.rollover_spend,
    budget_commander_control_spend: state => state.control_spend,
    budget_commander_excess_budget: state => state.excess_budget,
    budget_commander_emergency_stop: state => state.emergency_stop,
    budget_commander_budget: state => state.budget,
    budget_commander_kpi_option: state => state.kpi_option,
    budget_commander_kpi_target: state => state.kpi_target,
  },
  mutations: {
    SET_BUDGET_COMMANDER_DATA(state, payload) {
      state.response_data = payload['budget_commander_response_data'] || state.response_data;
      state.response = payload['budget_commander_response'] || state.response
      state.promise = payload['budget_commander_promise'] || state.promise
      state.budget = Number(payload['budget_commander_response_data'].budget) || state.budget
      state.excess_budget = Number(payload['budget_commander_response_data'].excess_budget) || state.excess_budget
      state.data_state = data_state;
    },
    SET_BUDGET_COMMANDER_BUDGET(state, budget){
      state.budget = budget
    },
    SET_BUDGET_COMMANDER_KPI_OPTION(state, kpi_option){
      state.kpi_option = kpi_option
    },
    SET_BUDGET_COMMANDER_KPI_TARGET(state, kpi_target){
      state.kpi_target = kpi_target
    },
    SET_BUDGET_COMMANDER_EXCESS_BUDGET(state, excess_budget){
      state.excess_budget = excess_budget
    },
    SET_BUDGET_COMMANDER_SETTINGS(state, payload) {
      state.notify_via_email = payload['notify_via_email']
      state.pause_campaigns = payload['pause_campaigns']
      state.enable_campaigns = payload['enable_campaigns']
      state.rollover_spend = payload['rollover_spend']
      state.control_spend = payload['control_spend']
      state.emergency_stop = payload['emergency_stop']
    }
   
  },

  actions: {

    getBudgetCommanderData({ commit, rootState,state }, payload) {
      const selected_account_id = rootState.selected_account.selected_account.account_id
      if(state.response_data.id!==selected_account_id){
        data_state.idle()//the user has switched account so start again in the cycle
      }
      
      if(data_state.isSuccess)return
      
      
      const account_id = payload['account_id']
      data_state.pending()
      
      let budget_commander_promise = axios.get('/api/account/'+account_id+'/bcgraph')

      budget_commander_promise.then(response => {

        let budget_commander_response_data = response.data

        commit('SET_BUDGET_COMMANDER_DATA',{
          'budget_commander_response_data' : budget_commander_response_data,
          'budget_commander_response': response.data,
          'budget_commander_promise' : budget_commander_promise
        })
        
        data_state.success()

      }).catch(error => {
          data_state.error()
          console.log(error)
      });

    },
    setBudgetCommanderSettings({ commit }, payload){

      commit('SET_BUDGET_COMMANDER_SETTINGS', payload)

    },
    setBudgetCommanderBudget({commit}, value){
      commit('SET_BUDGET_COMMANDER_BUDGET', value)
    },
    setBudgetCommanderKpiOption({commit}, value){
      commit('SET_BUDGET_COMMANDER_KPI_OPTION', value)
    },
    setBudgetCommanderKpiTarget({commit}, value){
      commit('SET_BUDGET_COMMANDER_KPI_TARGET', value)
    },
    setBudgetCommanderExcessBudget({commit}, value){
      commit('SET_BUDGET_COMMANDER_EXCESS_BUDGET', value)
    },
  
  }
}
