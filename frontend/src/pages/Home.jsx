import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, MapPin, Home as HomeIcon, ArrowRight, Sparkles, Building, Key } from 'lucide-react';
import { propertyService } from '../api';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);

  // Search states
  const [searchLocation, setSearchLocation] = useState('');
  const [propertyType, setPropertyType] = useState('');

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const response = await propertyService.getFeaturedProperties();
        // Handle pagination response if any, or direct list
        const data = response.data.results || response.data;
        setFeatured(data.slice(0, 3)); // show top 3 featured properties
      } catch (error) {
        console.error("Failed to fetch properties:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProperties();
  }, []);

  const handleSearch = (e) => {
    if (e) e.preventDefault();
    const params = new URLSearchParams();
    if (searchLocation) params.set('search', searchLocation);
    if (propertyType) params.set('property_type', propertyType);
    navigate(`/properties?${params.toString()}`);
  };

  const getImageUrl = (path) => {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';
    const baseUrl = API_URL.replace('/api/v1', '');
    return `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}`;
  };

  const formatPrice = (price, listType) => {
    const num = Number(price);
    if (isNaN(num)) return price;

    let formatted = '';
    if (num >= 10000000) {
      formatted = `₹${(num / 10000000).toFixed(2)} Cr`;
    } else if (num >= 100000) {
      formatted = `₹${(num / 100000).toFixed(2)} Lakh`;
    } else {
      formatted = `₹${num.toLocaleString('en-IN')}`;
    }

    if (listType === 'rent') {
      return `${formatted} / mo`;
    }
    return formatted;
  };

  return (
    <div className="home-page animate-fade-in">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-bg-glow"></div>
        <div className="container hero-content">
          <span className="badge glass">✨ AI-Powered Real Estate</span>
          <h1 className="hero-title">
            Find Your Dream Home With <br />
            <span className="gradient-text">Intelligent Search</span>
          </h1>
          <p className="hero-subtitle">
            Experience the future of real estate. Discover verified properties in major Indian cities with custom BHK layouts, luxury estates, and cozy studios.
          </p>

          <form onSubmit={handleSearch} className="search-bar glass-card">
            <div className="search-input-wrapper">
              <MapPin className="search-icon" size={20} />
              <input 
                type="text" 
                placeholder="Location (e.g., Mumbai, Delhi)..." 
                className="search-input" 
                value={searchLocation}
                onChange={(e) => setSearchLocation(e.target.value)}
              />
            </div>
            <div className="search-divider"></div>
            <div className="search-input-wrapper">
              <HomeIcon className="search-icon" size={20} />
              <select 
                className="search-select"
                value={propertyType}
                onChange={(e) => setPropertyType(e.target.value)}
              >
                <option value="">Property Type</option>
                <option value="apartment">Apartment</option>
                <option value="house">House / Villa</option>
                <option value="condo">Condo</option>
              </select>
            </div>
            <button type="submit" className="btn btn-primary search-btn">Search</button>
          </form>
        </div>
      </section>

      {/* Explore Residence & Discover Studio Section */}
      <section className="categories-section container section">
        <div className="section-header center">
          <h2>Discover Premium <span className="gradient-text">Categories</span></h2>
          <p className="section-subtitle">Find your niche from premium residence estates to high-comfort urban studios.</p>
        </div>

        <div className="categories-grid">
          {/* Explore Residence Estate */}
          <div 
            className="category-card glass-card large-card"
            style={{ backgroundImage: `linear-gradient(rgba(2, 6, 23, 0.4), rgba(2, 6, 23, 0.85)), url(${getImageUrl('/media/property_images/chennai_estate.png')})` }}
            onClick={() => navigate('/properties?property_type=house')}
          >
            <div className="category-tag">LIFESTYLE</div>
            <div className="category-content">
              <h3>Explore Residence Estates</h3>
              <p>Luxury independent houses and contemporary beach villas with private gardens, pools, and elite amenities.</p>
              <span className="category-link">View Estates <ArrowRight size={16} /></span>
            </div>
          </div>

          {/* Discover Studio */}
          <div 
            className="category-card glass-card large-card"
            style={{ backgroundImage: `linear-gradient(rgba(2, 6, 23, 0.4), rgba(2, 6, 23, 0.85)), url(${getImageUrl('/media/property_images/pune_studio.png')})` }}
            onClick={() => navigate('/properties?bedrooms=1&property_type=apartment')}
          >
            <div className="category-tag">URBAN LIVING</div>
            <div className="category-content">
              <h3>Discover Cozy Studios</h3>
              <p>Perfect for young professionals. Fully furnished and compact studio spaces situated in prime urban hubs.</p>
              <span className="category-link">View Studios <ArrowRight size={16} /></span>
            </div>
          </div>
        </div>

        {/* BHK Quick Filters */}
        <div className="bhk-specials">
          <h3>Indian BHK Specials</h3>
          <div className="bhk-grid">
            <div className="bhk-card glass-card" onClick={() => navigate('/properties?bedrooms=2')}>
              <Building size={24} className="bhk-icon" />
              <h4>2 BHK Apartments</h4>
              <p>Ideal family setups in premium high-rises.</p>
              <span className="bhk-arrow"><ArrowRight size={16} /></span>
            </div>
            <div className="bhk-card glass-card" onClick={() => navigate('/properties?bedrooms=3')}>
              <Sparkles size={24} className="bhk-icon" />
              <h4>3 BHK Residences</h4>
              <p>Expansive flats with scenic city balconies.</p>
              <span className="bhk-arrow"><ArrowRight size={16} /></span>
            </div>
            <div className="bhk-card glass-card" onClick={() => navigate('/properties?bedrooms=4')}>
              <Key size={24} className="bhk-icon" />
              <h4>4 BHK Luxury Estates</h4>
              <p>Elite villas for spacious, royal living.</p>
              <span className="bhk-arrow"><ArrowRight size={16} /></span>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Properties */}
      <section className="featured-section container section">
        <div className="section-header">
          <h2>Featured Properties</h2>
          <button className="btn btn-outline" onClick={() => navigate('/properties')}>
            View All <ArrowRight size={16} />
          </button>
        </div>

        {loading ? (
          <div className="loading-skeleton">Loading premium properties...</div>
        ) : (
          <div className="property-grid">
            {featured.length > 0 ? (
              featured.map(property => (
                <div key={property.id} className="property-card glass-card" onClick={() => navigate(`/properties?search=${property.city}`)}>
                  <div className="property-image-container">
                    {property.primary_image ? (
                      <img src={getImageUrl(property.primary_image)} alt={property.title} className="property-image" />
                    ) : (
                      <div className="property-image-placeholder">No Image</div>
                    )}
                    <div className="property-badge">{property.listing_type === 'sale' ? 'For Sale' : 'For Rent'}</div>
                  </div>
                  <div className="property-info">
                    <div className="property-price">{formatPrice(property.price, property.listing_type)}</div>
                    <h3 className="property-title">{property.title}</h3>
                    <p className="property-location"><MapPin size={14} /> {property.city}, {property.state}</p>
                    <div className="property-features">
                      <span>{property.bedrooms} BHK</span>
                      <span>•</span>
                      <span>{property.bathrooms} Baths</span>
                      <span>•</span>
                      <span>{Math.round(property.area_sqft)} sqft</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-properties glass">
                <p>No featured properties found. Check back later!</p>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default Home;
