/*
 * Adopted from The Open Source Geospatial Foundation
 
 *Extended by Mbani Benson tosimulate impacts of lake level changes on lakeshore towns of Kisumu and Kampala
 
 */

Ext.require([
    'Ext.container.Viewport',
    'Ext.layout.container.Border',
    'GeoExt.tree.Panel',
    'Ext.tree.plugin.TreeViewDragDrop',
    'GeoExt.panel.Map',
    'GeoExt.tree.OverlayLayerContainer',
    'GeoExt.tree.BaseLayerContainer',
    'GeoExt.data.LayerTreeModel',
    'GeoExt.tree.View',
    'GeoExt.tree.Column',
	'Ext.data.writer.Json',
    'Ext.grid.Panel',
    'GeoExt.data.reader.WmsCapabilities',
    'GeoExt.data.WmsCapabilitiesLayerStore',
	'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.tip.QuickTipManager',
    'Ext.ux.LiveSearchGridPanel'
	
]);

var mapPanel, tree, slr, layerPresent ;

layerPresent = 0;

function vSlider(){
  $( function() {
    $( "#grid" ).slider({
      orientation: "vertical",
      range: "min",
      min: 0,
      max: 12,
      value: 0,
	  step: 3,
            slide: function( event, ui ) {
        $( "#amount" ).val( ui.value + "  Meters ASL");
		if (ui.value == 12) {
			
			if (layerPresent==3 ||layerPresent==6 || layerPresent==9 || layerPresent==12 ){
				
				mapPanel.map.removeLayer(slr);
				
			}			
			
			slr = new OpenLayers.Layer.WMS("Inundation at 12 Meters",
                    "http://localhost:8080/geoserver/wms", {
                        layers: "cite:lakerise12",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        buffer: 0
                    }
                );
			


			mapPanel.map.addLayer(slr);
			layerPresent=12;
		}

		else if (ui.value == 9) {
			
			if (layerPresent==3 ||layerPresent==6 || layerPresent==9 || layerPresent==12 ){
				
				mapPanel.map.removeLayer(slr);
				
			}
			
			slr = new OpenLayers.Layer.WMS("Inundation at 9 Meters",
                    "http://localhost:8080/geoserver/wms", {
                        layers: "cite:lakerise9",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        buffer: 0
                    }
                );
			

			
			mapPanel.map.addLayer(slr);
			layerPresent=9;
		}
		
		
		else if (ui.value == 6) {
			
			
			if (layerPresent==3 ||layerPresent==6 || layerPresent==9 || layerPresent==12 ){
				
				mapPanel.map.removeLayer(slr);
				
			}
			
			slr = new OpenLayers.Layer.WMS("Inundation at 6 Meters",
                    "http://localhost:8080/geoserver/wms", {
                        layers: "cite:lakerise9",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        buffer: 0
                    }
                );
				
			
			
			mapPanel.map.addLayer(slr);
			layerPresent=6;
		}
		
		
		else if (ui.value == 3) { 
		
		
			if (layerPresent==3 ||layerPresent==6 || layerPresent==9 || layerPresent==12 ){
				
				mapPanel.map.removeLayer(slr);
				
			}
			
			slr = new OpenLayers.Layer.WMS("Inundation at 3 Meters",
                    "http://localhost:8080/geoserver/wms", {
                        layers: "cite:lakerise3",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        buffer: 0
                    }
                );

			
				
			mapPanel.map.addLayer(slr);
			layerPresent=3;
		}
		
		
		else if (ui.value == 0) { 
			
			if (layerPresent==3 ||layerPresent==6 || layerPresent==9 || layerPresent==12 ){
				
				mapPanel.map.removeLayer(slr);
				
			}
				
			//layerPresent = mapPanel.map.addLayer(slr);
			layerPresent=0;
		}
		
		
      }
    });
    $( "#amount" ).val( $( "#grid" ).slider( "value" ) + "  Meters ASL");
	} );
};


Ext.application(
{
    name: 'Tree',
    launch: function() {
        // create a map panel with some layers that we will show in our layer tree
        // below.
        mapPanel = Ext.create('GeoExt.panel.Map', {
            border: true,
            region: "center",
            // we do not want all overlays, to try the OverlayLayerContainer
            map: {allOverlays: false},
            center: [33.4384, -0.7558],
            zoom: 7,
            layers: [
                /*new OpenLayers.Layer.WMS("Blue Marble",
                    "http://demo.opengeo.org/geoserver/ows?", {
                        layers: "nasa:bluemarble",
                        format: "image/png8"
                    }, {
                        buffer: 0,
                        visibility: false
                    }
                ),*/
                new OpenLayers.Layer.WMS("OpenStreetMap WMS",
                    "https://ows.terrestris.de/osm/service?",
                    {layers: 'OSM-WMS'},
                    {
                        attribution: '&copy; terrestris GmbH & Co. KG <br>' +
                            'Data &copy; OpenStreetMap ' +
                            '<a href="http://www.openstreetmap.org/copyright/en"' +
                            'target="_blank">contributors<a>'
                    }
                ),
                new OpenLayers.Layer.WMS("Country Borders",
                    "https://ows.terrestris.de/geoserver/osm/wms", {
                        layers: "osm:osm-country-borders",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        resolutions: [
                            1.40625,
                            0.703125,
                            0.3515625,
                            0.17578125,
                            0.087890625,
                            0.0439453125,
                            0.02197265625,
                            0.010986328125,
                            0.0054931640625
                        ],
                        buffer: 0
                    }
                ),
                new OpenLayers.Layer.WMS("Gas Stations",
                    "https://ows.terrestris.de/geoserver/osm/wms", {
                        layers: "osm:osm-fuel",
                        transparent: true,
                        format: "image/png"
                    }, {
                        isBaseLayer: false,
                        buffer: 0
                    }
                ),
                new OpenLayers.Layer.WMS("Bus Stops",
                    "https://ows.terrestris.de/osm-haltestellen?",
                    {
                        layers: 'OSM-Bushaltestellen',
                        format: 'image/png',
                        transparent: true
                    },
                    {
                        singleTile: true,
                        visibility: false
                    }
                ),
                // create a group layer (with several layers in the "layers" param)
                // to show how the LayerParamLoader works
                new OpenLayers.Layer.WMS("Tasmania (Group Layer)",
                    "http://demo.opengeo.org/geoserver/wms", {
                        layers: [
                            "topp:tasmania_state_boundaries",
                            "topp:tasmania_water_bodies",
                            "topp:tasmania_cities",
                            "topp:tasmania_roads"
                        ],
                        transparent: true,
                        format: "image/gif"
                    }, {
                        isBaseLayer: false,
                        buffer: 0,
                        // exclude this layer from layer container nodes
                        displayInLayerSwitcher: false,
                        visibility: false
                    }
                )
            ]
        });

        // create our own layer node UI class, using the TreeNodeUIEventMixin
        //var LayerNodeUI = Ext.extend(GeoExt.tree.LayerNodeUI, new GeoExt.tree.TreeNodeUIEventMixin());

        /*var treeConfig = [
            {nodeType: 'gx_layercontainer', layerStore: map.layers}
        {
            nodeType: "gx_baselayercontainer"
        }, {
            nodeType: "gx_overlaylayercontainer",
            expanded: true,
            // render the nodes inside this container with a radio button,
            // and assign them the group "foo".
            loader: {
                baseAttrs: {
                    radioGroup: "foo",
                    uiProvider: "layernodeui"
                }
            }
        }, {
            nodeType: "gx_layer",
            layer: "Tasmania (Group Layer)",
            isLeaf: false,
            // create subnodes for the layers in the LAYERS param. If we assign
            // a loader to a LayerNode and do not provide a loader class, a
            // LayerParamLoader will be assumed.
            loader: {
                param: "LAYERS"
            }
        }];*/

        var store = Ext.create('Ext.data.TreeStore', {
            model: 'GeoExt.data.LayerTreeModel',
            root: {
                expanded: true,
                children: [
                    {
                        plugins: [{
                            ptype: 'gx_layercontainer',
                            store: mapPanel.layers
                        }],
                        expanded: true
                    }, {
                        plugins: ['gx_baselayercontainer'],
                        expanded: true,
                        text: "Base Maps"
                    }, {
                        plugins: ['gx_overlaylayercontainer'],
                        expanded: true
                    }
                ]
            }
        });

        var layer;

        // create the tree with the configuration from above
        tree = Ext.create('GeoExt.tree.Panel', {
            border: true,
            region: "west",
            title: "Layers",
            width: 250,
            split: true,
            collapsible: true,
            collapseMode: "mini",
            autoScroll: true,
            store: store,
            rootVisible: false,
            lines: false,
            tbar: [{
                text: "remove",
                handler: function() {
                    layer = mapPanel.map.layers[2];
                    mapPanel.map.removeLayer(layer);
                }
            }, {
                text: "add",
                handler: function() {
                    mapPanel.map.addLayer(layer);
                }
            }]
        });
		
		//slider
		/*Ext.create('Ext.slider.Single', {
		height: 200,
		value: 50,
		increment: 10,
		vertical: true,
		minValue: 0,
		maxValue: 100,
		renderTo: 'grid'
	});*/

	//end of slider

        Ext.create('Ext.Viewport', {
            layout: "fit",
            hideBorders: false,
            items: {
                layout: "border",
                deferredRender: false,
                items: [mapPanel, tree, {
                    contentEl: "grid",
                    region: "east",
                    bodyStyle: {"padding": "5px"},
                    collapsible: true,
                    collapseMode: "mini",
                    split: true,
                    width: 200,
                    title: "Description"
                },{
                    contentEl: "anothergrid",
                    region: "south",
                    bodyStyle: {"padding": "5px"},
                    collapsible: true,
                    collapseMode: "mini",
                    split: true,
                    height: 150,
                    title: "Available Geospatial Datasets"
                }]
            }
        });
    }
});


//wms capabilities loader
Ext.application({
    name: 'WMSGetCapabilities',
    launch: function() {

        // create a new WMS capabilities store
        store = Ext.create('GeoExt.data.WmsCapabilitiesStore', {
            storeId: 'wmscapsStore',
            url: "http://localhost:8080/geoserver/wms/filedata?request=GetCapabilities",
            autoLoad: true
        });

        // create a grid to display records from the store
        /*var grid = Ext.create('Ext.grid.Panel', {
            //title: "WMS Capabilities",
            store: Ext.data.StoreManager.lookup('wmscapsStore'),
            columns: [
                {header: "Title", dataIndex: "title", sortable: true},
                {header: "Name", dataIndex: "name", sortable: true},
                //{header: "Queryable", dataIndex: "queryable", sortable: true, width: 70},
                {id: "description", header: "Description", dataIndex: "abstract", flex: 1}
            ],
            renderTo: "anothergrid",
			plugins: 'gridfilters',
            height: 300,
            width: 1480,
            listeners: {
                itemdblclick: addLayer
            }
        });*/
		
		
		var grid = Ext.create('Ext.ux.LiveSearchGridPanel', {
        store: Ext.data.StoreManager.lookup('wmscapsStore'),
        columnLines: true,
        columns: [
                {header: "Title", dataIndex: "title", sortable: true},
                {header: "Name", dataIndex: "name", sortable: true},
                //{header: "Queryable", dataIndex: "queryable", sortable: true, width: 70},
                {id: "description", header: "Description", dataIndex: "abstract", flex: 1}
            ],
        height: 350,
        width: Ext.themeName === 'neptune-touch' || Ext.themeName === 'crisp' ? 1480 : 1480,
        //title: 'Live Search Grid',
        renderTo: 'anothergrid',
		listeners: {
                itemdblclick: addLayer
            },
        viewConfig: {
            stripeRows: true
        }
    });

	
	
		
		function addLayer (grid, record) {
			var layer = record.getLayer().clone();
			mapPanel.map.addLayer(layer);
		}
	}
});


