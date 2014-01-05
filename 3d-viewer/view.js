var canvas = document.getElementById('cv');
var viewer = new JSC3D.Viewer(canvas);

var components = ['stl/0.stl', 'stl/1.stl', 'stl/2.stl', 'stl/3.stl', 'stl/4.stl'];
var colors = [0xff0000, 0x0000ff, 0x00ff00, 0xffff00, 0x00ffff];
var theScene = new JSC3D.Scene;
var numOfLoaded = 0;

var onModelLoaded = function(scene) {
    var meshes = scene.getChildren();
    // there should be only one mesh for an STL
    for (var i=0; i<meshes.length; i++) {
        meshes[i].init();
        theScene.addChild(meshes[i]);
        //theScene.calcAABB();
        viewer.update();
        if (meshes.length > 0) {
            meshes[0].setMaterial(new JSC3D.Material('red-material', 0, colors[numOfLoaded]));
        }
    }
    if (++numOfLoaded == components.length)
        viewer.replaceScene(theScene);
};
for (var i=0; i<components.length; i++) {
	var loader = new JSC3D.StlLoader;
	loader.onload = onModelLoaded;
	loader.loadFromUrl(components[i]);
}

viewer.setParameter('BackgroundColor1', '#E5D7BA');
viewer.setParameter('BackgroundColor2', '#383840');
viewer.setParameter('Renderer', 'webgl');
viewer.init();
viewer.update();