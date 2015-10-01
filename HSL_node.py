#
#										    
#
#	created by Jordan Alphonso
#		on 7.25.2015
#
#



import maya.OpenMaya as om
import maya.OpenMayaMPx as MPx
import colorsys
import sys

kNodeName = "jaHSL"

class HSLnode( MPx.MPxNode ):

    kNodeId = om.MTypeId(0x00000220)

    #define attrs
    H =             om.MObject()
    S =             om.MObject()
    L =             om.MObject()
    inputColorR =   om.MObject()
    inputColorG =   om.MObject()
    inputColorB =   om.MObject()
    outputColorR =  om.MObject()
    outputColorG =  om.MObject()
    outputColorB =  om.MObject()
    outputColor =   om.MObject()
    inputColor =    om.MObject()

    #constructor
    def __init__( self ):
        MPx.MPxNode.__init__( self )


    #compute function
    def compute( self, plug, data ):

        #get inputs
        cR = data.inputValue( HSLnode.inputColorR ).asFloat()
        cG = data.inputValue( HSLnode.inputColorG ).asFloat()
        cB = data.inputValue( HSLnode.inputColorB ).asFloat()

        Hin = data.inputValue( HSLnode.H ).asFloat()
        Sin = data.inputValue( HSLnode.S ).asFloat()
        Lin = data.inputValue( HSLnode.L ).asFloat()

        #convert to hls
        HSLconvert = colorsys.rgb_to_hls( cR, cG, cB )
        newValueH = ( HSLconvert[0] ) + ( Hin / 2 )
        newValueL = ( HSLconvert[1] ) + Lin
        newValueS = ( HSLconvert[2] ) + Sin

        if newValueS <= 0:
            newValueS = 0

        #convert newValue back to RGB
        newColor = colorsys.hls_to_rgb( newValueH, newValueL, newValueS )

        #asssign new value to output color
        cOutR = data.outputValue( HSLnode.outputColorR )
        cOutG = data.outputValue( HSLnode.outputColorG )
        cOutB = data.outputValue( HSLnode.outputColorB )
        cOutR.setFloat( newColor[0] )
        cOutG.setFloat( newColor[1] )
        cOutB.setFloat( newColor[2] )

        data.setClean( plug )


#pointer
def nodeCreator():
    return MPx.asMPxPtr( HSLnode() )


#node initializer
def nodeInitializer():

    #create attributes
    nAttr = om.MFnNumericAttribute()

    #H
    HSLnode.H = nAttr.create( 'Hue', 'Hue', om.MFnNumericData.kFloat, 0.0 )
    nAttr.setKeyable( True )
    nAttr.setMin( -1.0 )
    nAttr.setMax( 1.0 )
    HSLnode.addAttribute( HSLnode.H )

    #S
    HSLnode.S = nAttr.create( 'Saturation', 'Saturation', om.MFnNumericData.kFloat, 0.0 )
    nAttr.setKeyable( True )
    nAttr.setMin( -1.0 )
    nAttr.setMax( 1.0 )
    HSLnode.addAttribute( HSLnode.S )

    #L
    HSLnode.L = nAttr.create( 'Lightness', 'Lightness', om.MFnNumericData.kFloat, 0.0 )
    nAttr.setKeyable( True )
    nAttr.setSoftMin( -1.0 )
    nAttr.setSoftMax( 1.0 )
    HSLnode.addAttribute( HSLnode.L )

    #input colorR
    HSLnode.inputColorR = nAttr.create( "ColorR", "ColorR", om.MFnNumericData.kFloat )
    nAttr.setKeyable( True )
    HSLnode.addAttribute( HSLnode.inputColorR )

    #input colorG
    HSLnode.inputColorG = nAttr.create( "ColorG", "ColorG", om.MFnNumericData.kFloat )
    nAttr.setKeyable( True )
    HSLnode.addAttribute( HSLnode.inputColorG )

    #input colorB
    HSLnode.inputColorB = nAttr.create( "ColorB", "ColorB", om.MFnNumericData.kFloat )
    nAttr.setKeyable( True )
    HSLnode.addAttribute( HSLnode.inputColorB )

    #input color
    HSLnode.inputColor = nAttr.create( "Color", "Color", HSLnode.inputColorR, HSLnode.inputColorG, HSLnode.inputColorB )
    nAttr.setUsedAsColor( True )
    HSLnode.addAttribute( HSLnode.inputColor )

    #output colorR
    HSLnode.outputColorR = nAttr.create( "outColorR", "outColorR", om.MFnNumericData.kFloat )
    nAttr.setKeyable( False )
    nAttr.setStorable( False )
    HSLnode.addAttribute( HSLnode.outputColorR )

    #output colorG
    HSLnode.outputColorG = nAttr.create( "outColorG", "outColorG", om.MFnNumericData.kFloat )
    nAttr.setKeyable( False )
    nAttr.setStorable( False )
    HSLnode.addAttribute( HSLnode.outputColorG )

    #output colorB
    HSLnode.outputColorB = nAttr.create( "outColorB", "outColorB", om.MFnNumericData.kFloat )
    nAttr.setKeyable( False )
    nAttr.setStorable( False )
    HSLnode.addAttribute( HSLnode.outputColorB )

    #output color
    HSLnode.outputColor = nAttr.create( "outColor", "outColor", HSLnode.outputColorR, HSLnode.outputColorG, HSLnode.outputColorB )
    nAttr.setStorable( False )
    nAttr.setKeyable( False )
    HSLnode.addAttribute( HSLnode.outputColor )

    #attributeAffects
    HSLnode.attributeAffects( HSLnode.H, HSLnode.outputColorR )
    HSLnode.attributeAffects( HSLnode.S, HSLnode.outputColorR )
    HSLnode.attributeAffects( HSLnode.L, HSLnode.outputColorR )
    HSLnode.attributeAffects( HSLnode.inputColor, HSLnode.outputColorR )
    HSLnode.attributeAffects( HSLnode.H, HSLnode.outputColorG )
    HSLnode.attributeAffects( HSLnode.S, HSLnode.outputColorG )
    HSLnode.attributeAffects( HSLnode.L, HSLnode.outputColorG )
    HSLnode.attributeAffects( HSLnode.inputColor, HSLnode.outputColorG )
    HSLnode.attributeAffects( HSLnode.H, HSLnode.outputColorB )
    HSLnode.attributeAffects( HSLnode.S, HSLnode.outputColorB )
    HSLnode.attributeAffects( HSLnode.L, HSLnode.outputColorB )
    HSLnode.attributeAffects( HSLnode.inputColor, HSLnode.outputColorB )


#initialize plugin
def initializePlugin( mobject ):
    mplugin = MPx.MFnPlugin( mobject )
    try:
        mplugin.registerNode( kNodeName, HSLnode.kNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to load plugin " + kNodeName + "\n" )


#uninitialize plugin
def uninitializePlugin( mobject ):
    mplugin = MPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( HSLnode.kNodeId )
    except:
        sys.stderr.write( "Failed to unload plugin " + kNodeName + "\n" )