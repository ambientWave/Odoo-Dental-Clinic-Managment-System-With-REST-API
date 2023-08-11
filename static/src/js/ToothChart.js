odoo.define('dental_clinic.PatientAppointmentToothChart', function(require) {
    'use strict';
    //    const Registries = require('point_of_sale.Registries');
       const {Component} = owl;
       const {useState} = owl.hooks;
       const { useListener } = require('web.custom_hooks');
       const FormRenderer = require("web.FormRenderer");
       const {ComponentWrapper} = require("web.OwlCompatibility");
       var session = require('web.session');


       class PatientAppointmentToothChart extends Component {
        
         constructor(model) {
             super(...arguments);
             let self = this;
             console.log(model);
           this.myState = useState({addedMarkedTooth: ["kh"]});
               useListener('click', this.updateChart);
               useListener('click', this.resetChart);
         }
         async mounted() {

            console.log("mounted");
            console.log(session);
            const polygonsArray = document.querySelectorAll("polygon,path");
            let toothNumberClassElements = document.querySelectorAll(".tooth_number_class")
            let toothNumberClassElementsInnerText = [];
            for(let element of toothNumberClassElements) {
               toothNumberClassElementsInnerText.push(element.textContent);
            }
            for(let element of polygonsArray) {
               element.classList.remove("marked");
               if(toothNumberClassElementsInnerText.some(x => x===element.id)) {
                  element.classList.add("marked");
               }
               toothNumberClassElementsInnerText.push(element.textContent);
            }

         //   useListener('click', (async () => {console.log("RenderViewww")}));
        //    console.log(polygonsArray);
           for (const polygon of polygonsArray) {
             polygon.onclick = (event) => {
            //    console.log(
            //      document.querySelector("select").options.selectedIndex
            //    );
               if (event.currentTarget.classList.contains("marked")) {
                 event.currentTarget.classList.remove("marked");
                 event.currentTarget.classList.add("unmarked");
               } else {
                 event.currentTarget.classList.add("marked");
                 event.currentTarget.classList.remove("unmarked");
               }
             };
           }
         }

         async resetChart() {
            console.log("newfunctionnnnnnnnn")
         }
         async updateChart() {


            console.log("You knocked?");
            const polygonsArray2 = document.querySelectorAll("polygon,path");
            console.log(polygonsArray2);
            let toothNumberClassElements = document.querySelectorAll(".tooth_number_class")
            console.log(toothNumberClassElements);
            let toothNumberClassElementsInnerText = [];
            for(let element of toothNumberClassElements) {
               toothNumberClassElementsInnerText.push(element.textContent);
            }
            for(let element of polygonsArray2) {
               element.classList.remove("marked");
               if(toothNumberClassElementsInnerText.some(x => x===element.id)) {
                  element.classList.add("marked");
               }
               toothNumberClassElementsInnerText.push(element.textContent);
            }

         //    let self = this;
         //    console.log("You knocked?");
         //    const polygonsArray2 = document.querySelectorAll("polygon,path");
         //   console.log(polygonsArray2);
         //   let procedureTableElement = document.querySelector('[name="procedure_line_id"]').lastChild.lastChild.lastChild.childNodes[1]
         //   console.log(procedureTableElement)
         //   let tableEntry = document.createElement('tr');
         // //   let newVar = ["sk", "sjdj"]
         // //   Object.assign(self.myState, { addedMarkedTooth: newVar})

         //    let addedMarkedToothArray = [];

         //    for(let element of polygonsArray2) {
         //       if(element.classList.contains("marked")) {
         //          if(addedMarkedToothArray.some(x => x!==element.textContent)) {
         //             addedMarkedToothArray.push(element.textContent);
         //             tableEntry.outerHTML = `<tr class="o_data_row" data-id="dental.procedure.line_6"><td class="o_data_cell o_field_cell tooth_number_class" tabindex="-1" title="${element.textContent}">${element.textContent}</td><td class="o_data_cell o_field_cell o_list_many2one o_required_modifier" tabindex="-1" title=""></td><td class="o_data_cell o_field_cell o_list_number o_readonly_modifier" tabindex="-1" title=""></td><td class="o_list_record_remove"><button class="fa fa-trash-o" name="delete" aria-label="Delete row 1"></button></td></tr>`
         //             procedureTableElement.prepend(tableEntry)
         //          }
                  

         //       }

         //    }

         //    let lastRunaddedMarkedToothArray = addedMarkedToothArray;

         //    let toothNumberClassElements = document.querySelectorAll(".tooth_number_class")
         //    console.log(toothNumberClassElements);
         //    let toothNumberClassElementsInnerText = [];
            
            this.rpc({
            model: 'patient.appointment',
            method: 'search_read',
            // args: [[['lst_price', '<=', "100"]]]
         //    args: [[this.state.data.partner_id.res_id]]
        }).then(wholeItemObject => {console.log(wholeItemObject)})

           this.rpc({
            model: 'dental.procedure.line',
            method: 'search_read',
        }).then(itemIdsArray => {console.log(itemIdsArray)
            console.log(this.env);
            console.log(this.state);});
            console.log(this);
            console.log(self);
            console.log(this.el);
            console.log(this.env)
            console.log(this.state); //this is an important object
            console.log(this.myState);
            };


            // async mounted() {
            //    console.log("mounted");
            //    console.log(session);
            //    useListener('click', (async () => {console.log("RenderViewww")}));
            //    const polygonsArray = document.querySelectorAll("polygon,path");
            // //    console.log(polygonsArray);
            //    for (const polygon of polygonsArray) {
            //      polygon.onclick = (event) => {
            //     //    console.log(
            //     //      document.querySelector("select").options.selectedIndex
            //     //    );
            //        if (event.currentTarget.classList.contains("marked")) {
            //          event.currentTarget.classList.remove("marked");
            //          // event.currentTarget.classList.add("unmarked");
            //        } else {
            //          event.currentTarget.classList.add("marked");
            //          // event.currentTarget.classList.remove("unmarked");
            //        }
            //      };
            //    }
            //  }      
      //    async updateChart() {
      //       console.log("You knocked?");
      //       const polygonsArray2 = document.querySelectorAll("polygon,path");
      //      console.log(polygonsArray2);
      //       let toothNumberClassElements = document.querySelectorAll(".tooth_number_class")
      //       console.log(toothNumberClassElements);
      //       let toothNumberClassElementsInnerText = [];
      //       for(let element of toothNumberClassElements) {
      //          toothNumberClassElementsInnerText.push(element.textContent);
      //       }
      //       for(let element of polygonsArray2) {
      //          element.classList.remove("marked");
      //          if(toothNumberClassElementsInnerText.some(x => x===element.id)) {
      //             element.classList.add("marked");
      //          }
      //          toothNumberClassElementsInnerText.push(element.textContent);
      //       }
      //       this.rpc({
      //       model: 'product.product',
      //       method: 'search_read',
      //       // args: [[['lst_price', '<=', "100"]]]
      //    //    args: [[this.state.data.partner_id.res_id]]
      //   }).then(wholeItemObject => {console.log(wholeItemObject)})

      //      this.rpc({
      //       model: 'product.product',
      //       method: 'search',
      //       args: [[['lst_price', '<=', "100"]]]
      //    //    args: [[this.state.data.partner_id.res_id]]
      //   }).then(itemIdsArray => {console.log(itemIdsArray)
      //       console.log(this.env);
      //       console.log(this.state);});
      //       console.log(this);
      //       console.log(self);
      //       console.log(this.el);
      //       console.log(this.env)
      //       console.log(this.state); //this is an important object
      //       console.log(this.myState);
      //       };
       };


       
       FormRenderer.include({
         
           async _renderView() {
               await this._super(...arguments);
               
               for(const element of this.el.querySelectorAll(".o_toothChart")) {
                //    console.log(this);
                //    console.log(self);
                //    console.log(this.el);
                //    console.log(this.env)
                //    console.log(this.state); //this is an important object
               //  let [...rest] = [this.state.data.procedure_line_id.res_ids]
                   this._rpc({
                       model: "dental.procedure.line",
                       method: "read",
                     //   method: "browse",
                     //   args: [[7]]
                       args: [[this.state.data.count]]
                   }).then(data => {(new ComponentWrapper(this, PatientAppointmentToothChart, useState(data[0]))
                       
                       ).mount(element);
                       console.log('00')
                       console.log(document.querySelectorAll("polygon,path"))
                       console.log('11');
                       console.log(this.element);
                       console.log('22');
                       console.log(element);
                       console.log('33');
                       console.log(data); //this is an important object
                       console.log('44');
                       var impEnv = this.env
                       console.log(this.env);
                       console.log('55');
                       var impState = this.state;
                       console.log(this.state);
                       useListener('click', ".o_td_label", (() => {console.log("RenderViewww22")}));
                   });
       
               }
       
       
           },
           
       });



       

    // const polygonsArray = document.querySelectorAll('polygon,path');
    // console.log(polygonsArray)
    //    for (const polygon of polygonsArray) {
    //      polygon.onclick = event => {
    //        console.log(document.querySelector('select').options.selectedIndex)
    //        if(event.currentTarget.classList.contains("marked")) {
    //          event.currentTarget.classList.remove('marked');
    //          event.currentTarget.classList.add('unmarked');
    //        } else {
    //          event.currentTarget.classList.add('marked');
    //         event.currentTarget.classList.remove('unmarked'); 
    //        };
           
           
    //      };
    //    }

       
        PatientAppointmentToothChart.template = 'PatientAppointmentFormToothChart';
    //    Registries.Component.add(SalesPartnerOrderSummary);
       return PatientAppointmentToothChart;
    });