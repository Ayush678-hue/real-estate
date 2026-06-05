import React, { useState, useEffect } from 'react';
import { Search, MapPin, Home as HomeIcon, ArrowRight } from 'lucide-react';
import { propertyService } from '../api';
import './Home.css';

const Home = () => {
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const response = await propertyService.getFeaturedProperties();
        setFeatured(response.data);
      } catch (error) {
        console.error("Failed to fetch properties:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProperties();
  }, []);

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
            Experience the future of real estate. Our AI understands your needs and 
            matches you with the perfect property instantly.
          </p>

          <div className="search-bar glass-card">
            <div className="search-input-wrapper">
              <MapPin className="search-icon" size={20} />
              <input type="text" placeholder="Location (e.g., Mumbai, Delhi)..." className="search-input" />
            </div>
            <div className="search-divider"></div>
            <div className="search-input-wrapper">
              <HomeIcon className="search-icon" size={20} />
              <select className="search-select">
                <option value="">Property Type</option>
                <option value="apartment">Apartment</option>
                <option value="house">House</option>
                <option value="villa">Villa</option>
              </select>
            </div>
            <button className="btn btn-primary search-btn">Search</button>
          </div>
        </div>
      </section>

      {/* Featured Properties */}
      <section className="featured-section container section">
        <div className="section-header">
          <h2>Featured Properties</h2>
          <button className="btn btn-outline">View All <ArrowRight size={16} /></button>
        </div>

        {loading ? (
          <div className="loading-skeleton">Loading premium properties...</div>
        ) : (
          <div className="property-grid">
            {featured.length > 0 ? (
              featured.map(property => (
                <div key={property.id} className="property-card glass-card">
                  <div className="property-image-container">
                    {property.primary_image ? (
                      <img src={property.primary_image} alt={property.title} className="property-image" />
                    ) : (
                      <div className="property-image-placeholder">No Image</div>
                    )}
                    <div className="property-badge">{property.listing_type === 'sale' ? 'For Sale' : 'For Rent'}</div>
                  </div>
                  <div className="property-info">
                    <div className="property-price">₹{Number(property.price).toLocaleString('en-IN')}</div>
                    <h3 className="property-title">{property.title}</h3>
                    <p className="property-location"><MapPin size={14} /> {property.city}, {property.state}</p>
                    <div className="property-features">
                      <span>{property.bedrooms} Beds</span>
                      <span>•</span>
                      <span>{property.bathrooms} Baths</span>
                      <span>•</span>
                      <span>{property.area_sqft} sqft</span>
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
