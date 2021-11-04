var cached_graph_def = {}
var tooltip_timeout = null

Vue.component('chartjs', {
    template:
    `<canvas  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style" :width="jp_props.width" height="jp_props.height"></canvas>`,
    methods: {
        graphjs_create(){
            console.log("create graph");
            var id = this.$props.jp_props.id.toString();
            console.log("create graph ", id);
            var canvas = document.getElementById(id);
            console.log("create graph : canvas");
            ctx = canvas.getContext('2d');
            console.log("create graph : ctx");
            var c = new Chart(ctx, this.$props.jp_props.def);
            console.log("create graph : c");
            cached_graph_def['chart'+id] = c;
            console.log("create graph : cache");
            cached_graph_def[this.$props.jp_props.id] = JSON.stringify(this.$props.jp_props.def);
            console.log("create graph : def");
            c.update()
            console.log("create graph : update");
        },
        graphjs_update() {
            var id = this.$props.jp_props.id.toString();
            c = cached_graph_def['chart'+id];
            c.update()
            //chart.update(this.$props.jp_props.def, true, true, this.$props.jp_props.update_animation); //Look into chart.update
        },
        graphjs_destroy() {
            var id = this.$props.jp_props.id.toString();
            c = cached_graph_def['chart'+id];
            c.destroy();
            
        }
    },
    
    mounted() {
        console.log("mounted");
        this.graphjs_create();
    },
    updated() {
        console.log("updated called ",   this.$props.jp_props.update_create);
        console.log("updated called:cache ",   this.$props.jp_props.use_cache);
        console.log("updated called:id ",   this.$props.jp_props.id);
        const container = this.$props.jp_props.id.toString();
        const chart = cached_graph_def['chart' + container];
        console.log("updated called:id ",    chart);
        if (!this.$props.jp_props.use_cache || (JSON.stringify(this.$props.jp_props.def) != cached_graph_def[this.$props.jp_props.id])) {
            cached_graph_def[this.$props.jp_props.id] = JSON.stringify(this.$props.jp_props.def);
            if (this.$props.jp_props.update_create) {
                //console.log("this is a new graph")
                this.graphjs_destroy();
                this.graphjs_create();
            } else {
                //console.log("this is an update")
                if (chart == null){
                    console.log("chart is null");
                }
                else{
                    this.graphjs_update();
                }
                //chart.update(this.$props.jp_props.def, true, true, this.$props.jp_props.update_animation); //Look into chart.update
            }
        }

    },
    props: {
        jp_props: Object
    }
});
